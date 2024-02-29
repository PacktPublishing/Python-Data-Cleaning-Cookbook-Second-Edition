# import pandas, numpy, and matplotlib
import pandas as pd
#import matplotlib.pyplot as plt
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe

pd.set_option('display.width', 70)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 20)
pd.options.display.float_format = '{:,.0f}'.format

covidtotals = pd.read_csv("data/covidtotals.csv",
  parse_dates=['lastdate'])
covidtotals.set_index("iso_code", inplace=True)

llm = OpenAI(api_token="Your API key")
type(llm)

covidtotalssdf = SmartDataframe(covidtotals, config={"llm": llm})
type(covidtotalssdf)


covidtotalssdf.chat("Show me some information about the data")

covidtotalssdf.chat("Show first five rows.")

covidtotalssdf.chat("Show total cases for locations with the five most total cases.")

covidtotalssdf.chat("Show total cases pm, total deaths pm, and location for locations with the 10 highest total cases pm.")

covidtotalsabb = covidtotalssdf.chat("Select total cases pm, total deaths pm, and location.")
covidtotalsabb

covidtotalsabb = covidtotalssdf.chat("Grab total cases pm, total deaths pm, and location.")
covidtotalsabb

covidtotalssdf.chat("Show total cases pm and location where total cases pm greater than 95th percentile.")

covidtotalssdf.chat("Summarize values for total cases pm and total deaths pm.").T

covidtotalssdf.chat("Show sum of total cases and total deaths by region.")

covidtotalssdf.chat("Plot the total_cases_pm column data distribution")

covidtotalssdf.chat("Plot the total_cases_pm data distribution")


covidtotalssdf.chat( "Plot total cases pm values against total deaths pm values")

covidtotalssdf.chat( "Plot total cases pm values against total deaths pm values with line")

covidtotalssdf.chat( "Plot total cases pm values against total deaths pm values with lmplot without extreme values")


covidtotalssdf.chat("Use regplot to show total deaths pm against total cases pm")

covidtotalssdf.chat("Use regplot to show total deaths pm against total cases pm without extreme values")

