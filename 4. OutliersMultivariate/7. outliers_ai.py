import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
llm = OpenAI(api_token="Your API key")

pd.set_option('display.width', 70)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 220)
pd.options.display.float_format = '{:,.0f}'.format

# load the data frames and create a smart data frame object
covidtotals = pd.read_csv("data/covidtotals.csv")

covidtotalssdf = SmartDataframe(covidtotals, config={"llm": llm})

# run some queries
covidtotalssdf.chat("Plot histogram of total cases per million")

covidtotalssdf.chat("Show boxplot of total cases per million")

covidtotalssdf.chat("regplot total_deaths_pm on total_cases_pm")

covidtotalssdf.chat("Show total cases per million 7 highest values and 7 lowest values of total cases per million sorted by total cases per million")

covidtotalssdf.chat("Show total cases per million for locations with highest total cases per million in each region")

covidtotalssdf.chat("Show total cases per million and total deaths per million for locationss with high total_cases_pm and low total_deaths_pm")

covidtotalssdf.chat("What variables are highly correlated with total cases")

