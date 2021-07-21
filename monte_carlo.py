import pandas as pd
import numpy as np
import numpy_financial as npf

class NormalDistribution:
  @staticmethod
  def generate(center, scale, size):
    return np.random.normal(center, scale, size).round(2)

class MonteCarlo:
  def __init__(self, std_dev, revenue, gross_margin_avg, operating_margin_avg, num_shares, num_simulations, num_years, dcf, peg):
    self.std_dev = std_dev
    self.revenue = revenue
    self.gross_margin_avg = gross_margin_avg
    self.operating_margin_avg = operating_margin_avg
    self.num_shares = num_shares
    self.num_simulations = num_simulations
    self.num_years = num_years
    self.dcf = dcf
    self.peg = peg

  def calculate(self):
    gross_margin = NormalDistribution.generate(self.gross_margin_avg, self.std_dev, self.num_years)
    operating_margin = NormalDistribution.generate(self.operating_margin_avg, self.std_dev, self.num_years)
    revenue_modifier = NormalDistribution.generate(1, self.std_dev, self.num_years)

    df = pd.DataFrame(index=range(self.num_years), data={
      "revenue": self.revenue * revenue_modifier,
      "gross_margin": gross_margin,
      "operating_margin": operating_margin
    })

    df["gross_profit"] = df["revenue"] * df["gross_margin"]
    df["operating_profit"] = df["revenue"] * df["operating_margin"]
    df["net_income"] = df["operating_profit"].apply(lambda x: self.dcf.calculate_tax(x))
    df["eps"] = df["net_income"].apply(lambda x: self.dcf.to_billions(x)) / self.num_shares

    return df

  def derive_pe(self, incomes):
    i = 0
    growth_pct = 0
    while i < incomes.size - 1:
      if incomes[i] > 0 and incomes[i + 1] > 0:
        change = incomes[i + 1] - incomes[i]
        growth_pct += change / incomes[i]
      i += 1
    
    avg_growth_pct = growth_pct / incomes.size
    new_pe = avg_growth_pct * self.peg * 100

    return avg_growth_pct, new_pe

  def simulate(self):
    financials = []

    for i in range(self.num_simulations):
      if i % 100 == 0:
        print(".", end="", flush=True)

      df = self.calculate()

      eps = df['eps']

      avg_growth_pct, derived_pe = self.derive_pe(df["net_income"])

      pe_multiple = NormalDistribution.generate(derived_pe, 0.3, 1)[0]

      financials.append([df['revenue'].mean().round(2),
                        df['gross_margin'].mean().round(2),
                        df['operating_margin'].mean().round(2),
                        df['gross_profit'].mean().round(2),
                        df['operating_profit'].mean().round(2),
                        df['net_income'].mean().round(2),
                        eps.mean().round(2),
                        pe_multiple,
                        npf.npv(self.dcf.discount_rate, eps[:eps.size].append(eps[-1:]) * pe_multiple)])
    
    return financials
