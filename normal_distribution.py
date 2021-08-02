import numpy as np

class NormalDistribution:
  def __init__(self, std_dev):
    self.std_dev = std_dev

  def generate(self, center, size):
    return np.random.normal(center, self.std_dev, size).round(2)
