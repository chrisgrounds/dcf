import json
from yahoo_fin import stock_info
from dcf import DCF
import numpy_financial as npf

num_years = 10
std_dev = 0.05
tax_rate = 0.2
peg = 1

def handler(event, context):
  queryStrings = event["queryStringParameters"]

  ticker = queryStrings.get("ticker")
  growth_rate = float(queryStrings.get("growth_rate", 1.5))
  operating_margin = float(queryStrings.get("operating_margin", 0.1))
  discount_rate = float(queryStrings.get("discount_rate", 0.15))
  perpetual_rate = float(queryStrings.get("perpetual_rate", 1.03))

  num_shares = stock_info.get_quote_data(ticker)["sharesOutstanding"]
  current_revenue = stock_info.get_income_statement(ticker).loc["totalRevenue"][0]
  dcf = DCF(current_revenue, std_dev, tax_rate, num_years, 2, operating_margin, num_shares, growth_rate, discount_rate, peg, perpetual_rate)

  df = dcf.calculate(distribution=False)

  eps = df['eps']

  derived_pe = dcf.derive_pe(df["net_income"])

  pe_multiple = derived_pe

  return {
    "statusCode": 200,
    "headers": {
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json"
    },
    "body": json.dumps({
      "revenue": df['revenue'].to_list(),
      "net_income": df["net_income"].to_list(),
      "eps": eps.to_list(),
      "pe_multiple": pe_multiple,
      "dcf_value": npf.npv(dcf.discount_rate, eps[:eps.size].append(eps[-1:]) * pe_multiple)
    })
  }
