# import pandas and load the covid data and land temperature data
import pandas as pd
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 12)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format

coviddaily = pd.read_csv("data/coviddaily.csv",
  parse_dates=["casedate"])
ltbrazil = pd.read_csv("data/ltbrazil.csv")

coviddailytotals = \
  pd.pivot_table(coviddaily.loc[coviddaily.casedate. \
  between('2023-02-01','2024-01-31')], 
  values=['new_cases','new_deaths'], index='casedate', 
  aggfunc='sum')

coviddailytotals.head(10)

# create a data frame with average temperatures from each station in Brazil
ltbrazil = ltbrazil.dropna(subset=['temperature'])

ltbrazilavgs = \
  pd.pivot_table(ltbrazil, index=['station'], 
  aggfunc={'latabs':'first','elevation':'first',
  'temperature':'mean'})

ltbrazilavgs.head(10)

