import argparse
import os
import pandas as pd
from generate import generate

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
std_dev = 0.05
tax_rate = 0.2
discount_rate = 0.15
peg = 1

def main():
  financials = generate(ticker, tax_rate, num_years, growth_rate, std_dev, gross_margin_avg, operating_margin_avg, args.simulations, discount_rate, peg)

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
