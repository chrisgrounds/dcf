import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Command line args')

parser.add_argument('--ticker')

args = parser.parse_args()

results_df = pd.read_csv("simulations/{}.csv".format(args.ticker))

print(results_df)

graph = results_df.plot(kind='hist', bins=500, y=["Discounted Cash Flow"], title="Discounted Cash Flow - Monte Carlo Simulation")
graph.set_xlabel("$ / share")
plt.show()
