import numpy as np

class DCF:
  def __init__(self, revenue, tax_rate, num_years, growth_rate, discount_rate):
    self.revenue = revenue
    self.tax_rate = tax_rate
    self.num_years = num_years
    self.growth_rate = growth_rate
    self.discount_rate = discount_rate

  def calculate_tax(self, v):
    return v * self.tax_rate if v > 0 else 0

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