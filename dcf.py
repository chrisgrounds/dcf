import pandas as pd
import numpy as np
import numpy_financial as npf
import argparse
from yahoo_fin import stock_info

parser = argparse.ArgumentParser(description='Command line args')

parser.add_argument('--simulations', type=int)
parser.add_argument('--ticker')
parser.add_argument('--growth', type=float)

args = parser.parse_args()
ticker = args.ticker
growth_rate = args.growth
gross_margin_avg = 0.2
operating_margin_avg = 0.1
std_dev = 0.1
tax_rate = 0.2
discount_rate = 0.07
pe_ratio = 30
num_years = 10

class Financials():
  @staticmethod
  def calculate_tax(v):
    return v * tax_rate if v > 0 else 0

  @staticmethod
  def to_billions(v):
    return v * 1000000000

  def from_billions(v):
    return v / 1000000000

  @staticmethod
  def generate_future_revenue(rev, growth_rate):
    revenue = [rev]

    i = 0
    while (i < num_years):
      revenue.append(round(revenue[-1] * growth_rate, 2))
      i += 1

    return np.array(revenue)

class NormalDistribution:
  @staticmethod
  def generate(center, scale, size):
    return np.random.normal(center, scale, size).round(2)

class MonteCarlo:
  def __init__(self, std_dev, revenue, gross_margin_avg, operating_margin_avg, num_shares):
    self.std_dev = std_dev
    self.revenue = revenue
    self.gross_margin_avg = gross_margin_avg
    self.operating_margin_avg = operating_margin_avg
    self.num_shares = num_shares

  def calculate(self):
    gross_margin = NormalDistribution.generate(self.gross_margin_avg, self.std_dev, num_years)
    operating_margin = NormalDistribution.generate(self.operating_margin_avg, self.std_dev, num_years)
    revenue_modifier = NormalDistribution.generate(1, self.std_dev, num_years)

    df = pd.DataFrame(index=range(num_years), data={
      "revenue": self.revenue * revenue_modifier,
      "gross_margin": gross_margin,
      "operating_margin": operating_margin
    })

    df["gross_profit"] = df["revenue"] * df["gross_margin"]
    df["operating_profit"] = df["revenue"] * df["operating_margin"]
    df["net_income"] = df["operating_profit"].apply(Financials.calculate_tax)
    df["eps"] = df["net_income"].apply(Financials.to_billions) / self.num_shares

    return df

  def simulate(self):
    financials = []

    for i in range(args.simulations):
      if i % 100 == 0:
        print(".", end="", flush=True)

      df = self.calculate()

      eps = df['eps']
      pe_multiple = NormalDistribution.generate(pe_ratio, 0.3, 1)[0]

      financials.append([df['revenue'].mean().round(2),
                        df['gross_margin'].mean().round(2),
                        df['operating_margin'].mean().round(2),
                        df['gross_profit'].mean().round(2),
                        df['operating_profit'].mean().round(2),
                        df['net_income'].mean().round(2),
                        eps.mean().round(2),
                        pe_multiple,
                        npf.npv(discount_rate, eps[:eps.size].append(eps[-1:]) * pe_multiple)])
    
    return financials

def main():
  num_shares = stock_info.get_quote_data(ticker)["sharesOutstanding"]
  current_revenue = Financials.from_billions(stock_info.get_income_statement(ticker).loc["totalRevenue"][0])
  revenue = Financials.generate_future_revenue(current_revenue, growth_rate)

  print("Generated revenue: ", revenue)

  monteCarlo = MonteCarlo(std_dev, revenue, gross_margin_avg, operating_margin_avg, num_shares)

  financials = monteCarlo.simulate()

  print("\n\nFinished simulation")

  results = pd.DataFrame.from_records(financials, columns=[
    'Revenue',
    'Gross Margin',
    'Operating Margin',
    'Gross Profit',
    'Operating Profit',
    'Net Income',
    'EPS',
    'PE Ratio',
    'Discounted Cash Flow'
  ])

  results.to_csv("simulations/{}/{}.csv".format(ticker, ticker))

if __name__ == "__main__":
  main()
