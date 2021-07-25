import numpy as np

class NormalDistribution:
  @staticmethod
  def generate(center, scale, size):
    return np.random.normal(center, scale, size).round(2)
