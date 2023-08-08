# import pandas, numpy, and matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

pd.set_option('display.width', 53)
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 20)
pd.options.display.float_format = '{:,.0f}'.format

covidtotals = pd.read_csv("data/covidtotals720.csv",
  parse_dates=['lastdate'])
covidtotals.set_index("iso_code", inplace=True)

# create a PandasAI object
llm = OpenAI(api_token="Your API key")

pandas_ai = PandasAI(llm)

pandas_ai.run(covidtotals, "Show first two rows.").T

pandas_ai.run(covidtotals, "Show column types.")

pandas_ai.run(covidtotals, "Show total cases for locations with the most.")


pandas_ai.run(covidtotals, "Show total cases pm, total deaths pm, and location for locations with the 10 highest total cases pm.")

covidtotalsabb = pandas_ai.run(covidtotals, "Select total cases pm, total deaths pm, and location.")
covidtotalsabb

covidtotalsabb = pandas_ai.run(covidtotals, "Grab total cases pm, total deaths pm, and location.")
covidtotalsabb

pandas_ai.run(covidtotals, "Show total cases pm and location where total cases pm greater than 95th percentile.")

pandas_ai.run(covidtotals, "Show the distribution of total cases pm and total deaths pm.")

pandas_ai.run(covidtotals, "Show sum of total cases and total deaths.")

pandas_ai.run(covidtotals, "Show sum of total cases and total deaths by region.")

pandas_ai.run(covidtotals, "Plot a histogram of total cases pm")

pandas_ai.run(covidtotals, "Plot total cases pm by total deaths pm")

pandas_ai.run(covidtotals, "Use regplot to show total deaths pm by total cases pm")

pandas_ai.run(covidtotals, "Use regplot to show total deaths pm by total cases pm without extreme values")
