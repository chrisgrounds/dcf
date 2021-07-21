import argparse
import os
import pandas as pd
from yahoo_fin import stock_info
from dcf import DCF
from monte_carlo import MonteCarlo

parser = argparse.ArgumentParser(description='Command line args')

parser.add_argument('--simulations', type=int)
parser.add_argument('--ticker')
parser.add_argument('--growth', type=float)
parser.add_argument('--years', type=int)

args = parser.parse_args()
ticker = args.ticker
growth_rate = args.growth
num_years = args.years
gross_margin_avg = 0.2
operating_margin_avg = 0.1
std_dev = 0.1
tax_rate = 0.2
discount_rate = 0.07
pe_ratio = 30

def main():
  num_shares = stock_info.get_quote_data(ticker)["sharesOutstanding"]
  current_revenue = stock_info.get_income_statement(ticker).loc["totalRevenue"][0] / 1000000 # refactor
  dcf = DCF(current_revenue, tax_rate, num_years, growth_rate)
  revenue = dcf.generate_future_revenue()

  print("Generated revenue: ", revenue)

  monteCarlo = MonteCarlo(std_dev, revenue, gross_margin_avg, operating_margin_avg, num_shares, args.simulations, num_years, dcf)

  financials = monteCarlo.simulate(pe_ratio, discount_rate)

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

  directory = "simulations/{}".format(ticker)

  if not os.path.exists(directory):
    os.makedirs(directory)

  results.to_csv("{}/{}.csv".format(directory, ticker))

if __name__ == "__main__":
  main()
