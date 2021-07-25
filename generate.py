from yahoo_fin import stock_info
from dcf import DCF
from monte_carlo import MonteCarlo

def generate(ticker, tax_rate, num_years, growth_rate, std_dev, gross_margin_avg, operating_margin_avg, simulations, discount_rate, peg):
  num_shares = stock_info.get_quote_data(ticker)["sharesOutstanding"]
  current_revenue = stock_info.get_income_statement(ticker).loc["totalRevenue"][0] / 1000000 # refactor
  dcf = DCF(current_revenue, tax_rate, num_years, growth_rate, discount_rate, peg)
  revenue = dcf.generate_future_revenue()

  print("Generated revenue: ", revenue)

  monteCarlo = MonteCarlo(std_dev, revenue, gross_margin_avg, operating_margin_avg, num_shares, simulations, num_years, dcf)

  return monteCarlo.simulate()
