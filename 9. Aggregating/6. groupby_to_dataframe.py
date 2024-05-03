# import pandas and load the covid data and land temperature data
import pandas as pd
pd.set_option('display.width', 62)
pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 50)
pd.options.display.float_format = '{:,.0f}'.format
coviddaily = pd.read_csv("data/coviddaily.csv", parse_dates=["casedate"])
ltbrazil = pd.read_csv("data/ltbrazil.csv")

coviddaily[['location','casedate',
  'new_cases','new_deaths']]. \
  set_index(['location','casedate']). \
  sample(10, random_state=1)

# convert covid data from one country per day to summary values across all countries per day
coviddailytotals = coviddaily.loc[coviddaily.\
  casedate.between('2023-02-01','2024-01-31')].\
  groupby(['casedate'], as_index=False)\
  [['new_cases','new_deaths']].\
  sum()

coviddailytotals.head(10)

# create a data frame with average temperatures from each station in Brazil
ltbrazil = ltbrazil.dropna(subset=['temperature'])
ltbrazilavgs = ltbrazil.groupby(['station'],
  as_index=False).\
  agg({'latabs':'first','elevation':'first',
  'temperature':'mean'})
ltbrazilavgs.head(10)

