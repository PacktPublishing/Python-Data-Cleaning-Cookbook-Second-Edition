# import pandas, numpy, and matplotlib
import pandas as pd
import numpy as np
pd.set_option('display.width', 70)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 100)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97g.csv",
    low_memory=False)
nls97.set_index("personid", inplace=True)
covidtotals = pd.read_csv("data/covidtotalswithmissings.csv",
    low_memory=False)

covidtotals.set_index("iso_code", inplace=True)

# check the demographic columns for missing
covidtotals.shape
demovars = ['pop_density','aged_65_older',
   'gdp_per_capita','life_expectancy','hum_dev_ind']
covidtotals[demovars].isnull().sum(axis=0)
demovarsmisscnt = covidtotals[demovars].isnull().sum(axis=1)
demovarsmisscnt.value_counts().sort_index()
covidtotals.loc[demovarsmisscnt>=4, ['location'] + demovars].\
  sample(5, random_state=1).T

# check the cumulative columns for missing
totvars = ['location','total_cases_pm','total_deaths_pm']
covidtotals[totvars].isnull().sum(axis=0)
totvarsmisscnt = covidtotals[totvars].isnull().sum(axis=1)
totvarsmisscnt.value_counts().sort_index()

# set logical missings to actual missings
nlsparents = nls97.iloc[:,-4:]
nlsparents.loc[nlsparents.motherhighgrade.between(-5,-1),
   'motherhighgrade'].value_counts()
nlsparents.loc[nlsparents.transform(lambda x: x.between(-5,-1)).\
  any(axis=1)]

nlsparents.transform(lambda x: x.between(-5,-1)).sum()

nlsparents.replace(list(range(-5,0)), np.nan, inplace=True)
nlsparents.isnull().sum()
