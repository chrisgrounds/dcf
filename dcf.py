import numpy as np

class DCF:
  def __init__(self, revenue, tax_rate, num_years, growth_rate, discount_rate, peg):
    self.revenue = revenue
    self.tax_rate = tax_rate
    self.num_years = num_years
    self.growth_rate = growth_rate
    self.discount_rate = discount_rate
    self.perceptual_growth_rate = 1.04
    self.peg = peg

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

    return ((perceptual_pe * 4) + growth_pe) / 5

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