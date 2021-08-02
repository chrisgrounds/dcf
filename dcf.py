import numpy as np
import pandas as pd
from normal_distribution import NormalDistribution

class DCF:
  def __init__(self, revenue, std_dev, tax_rate, num_years, gross_margin_avg, operating_margin_avg, num_shares, growth_rate, discount_rate, peg):
    self.revenue = revenue
    self.std_dev = std_dev
    self.tax_rate = tax_rate
    self.num_years = num_years
    self.gross_margin_avg = gross_margin_avg
    self.operating_margin_avg = operating_margin_avg
    self.num_shares = num_shares
    self.growth_rate = growth_rate
    self.discount_rate = discount_rate
    self.perceptual_growth_rate = 1.04
    self.peg = peg
    self.future_revenue = self.generate_future_revenue()
    self.normal = NormalDistribution(std_dev)
    print("Generated revenue: ", self.future_revenue)

  def calculate(self, distribution=True):
    if distribution:
      gross_margin = self.normal.generate(self.gross_margin_avg, self.num_years)
      operating_margin = self.normal.generate(self.operating_margin_avg, self.num_years)
      revenue_modifier = self.normal.generate(1, self.num_years)
    else:
      gross_margin = self.gross_margin_avg
      operating_margin = self.operating_margin_avg
      revenue_modifier = 1

    df = pd.DataFrame(index=range(self.num_years), data={
      "revenue": self.future_revenue * revenue_modifier,
      "gross_margin": gross_margin,
      "operating_margin": operating_margin
    })

    df["gross_profit"] = df["revenue"] * df["gross_margin"]
    df["operating_profit"] = df["revenue"] * df["operating_margin"]
    df["net_income"] = df["operating_profit"].apply(lambda x: self.calculate_tax(x))
    df["eps"] = df["net_income"].apply(lambda x: self.to_billions(x)) / self.num_shares

    return df

  def calculate_tax(self, v):
    return v * self.tax_rate if v > 0 else 0

  def derive_PE_from_perpeptual_growth(self):
    return self.perceptual_growth_rate / ((1 + self.discount_rate) - self.perceptual_growth_rate)

  def derive_PE_from_earnings_growth(self, incomes):
    i = 0
    growth_pct = 0

    while i < incomes.size - 1:
      if incomes[i] > 0 and incomes[i + 1] > 0:
        change = incomes[i + 1] - incomes[i]
        growth_pct += change / incomes[i]
      i += 1

    avg_growth_pct = growth_pct / incomes.size
    return avg_growth_pct * self.peg * 100

  def derive_pe(self, incomes):
    perceptual_pe = self.derive_PE_from_perpeptual_growth()
    growth_pe = self.derive_PE_from_earnings_growth(incomes)

    return (perceptual_pe + growth_pe) / 2

  def generate_future_revenue(self):
    revenue = []

    i = 0
    while (i < self.num_years):
      r = revenue[-1] if i != 0 else self.revenue
      revenue.append(round(r * self.growth_rate, 2))
      i += 1

    return np.array(revenue)

  def to_billions(self, v):
    return v * 1000000

  def from_billions(self, v):
    return v / 1000000