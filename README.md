# Discounted Cash Flow Monte Carlo Model

![example simulation](https://github.com/chrisgrounds/dcf-monte-carlo/blob/main/simulations/tsla/tsla.png)

## Generate DCF Model

This runs a Monte Carlo DCF simulation for the number of simulations specified and outputs it to `simulations/{ticker}/`.

```bash
python3 cli.py --simulations 100000 --ticker tsla --growth 1.5 --years 10
```

## Generate Histogram of Model

This prints out the dataframe stored in `simulations/{ticker}/` and generates the histogram.

```bash
python3 chart.py --ticker tsla
```
