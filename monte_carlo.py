import numpy_financial as npf
from normal_distribution import NormalDistribution

class MonteCarlo:
  def __init__(self, num_simulations, dcf):
    self.num_simulations = num_simulations
    self.dcf = dcf

  def simulate(self):
    financials = []

    for i in range(self.num_simulations):
      if i % 100 == 0:
        print(".", end="", flush=True)

      df = self.dcf.calculate()

      eps = df['eps']

      derived_pe = self.dcf.derive_pe(df["net_income"])

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
