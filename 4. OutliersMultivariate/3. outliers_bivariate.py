# import pandas, numpy, and matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.width', 55)
pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 20)
pd.options.display.float_format = '{:,.2f}'.format
covidtotals = pd.read_csv("data/covidtotals720.csv")
covidtotals.set_index("iso_code", inplace=True)

# set up the cumulative and demographic columns
totvars = ['location','total_cases',
  'total_deaths','total_cases_pm',
  'total_deaths_pm']
demovars = ['population','pop_density',
  'median_age','gdp_per_capita',
   'hosp_beds']

# generate a correlation matrix of the cumulative and demographic data
covidtotals.corr(method="pearson")

# get descriptive statistics on the cumulative values
covidtotalsonly = covidtotals.loc[:, totvars]

# see if some countries have unexpected low or high death rates given number of cases
covidtotalsonly['total_cases_q'] = pd.\
  qcut(covidtotalsonly['total_cases'],
  labels=['very low','low','medium',
  'high','very high'], q=5, precision=0)
covidtotalsonly['total_deaths_q'] = pd.\
  qcut(covidtotalsonly['total_deaths'],
  labels=['very low','low','medium',
  'high','very high'], q=5, precision=0)

pd.crosstab(covidtotalsonly.total_cases_q,
  covidtotalsonly.total_deaths_q)

covidtotals.loc[(covidtotalsonly. \
  total_cases_q=="very high") & \
  (covidtotalsonly.total_deaths_q=="low")].T
covidtotals.hosp_beds.mean()

# do a scatterplot of total_cases by total_deaths
ax = sns.regplot(x=covidtotals.total_cases/1000, y=covidtotals.total_deaths)
ax.set(xlabel="Cases (thousands)", ylabel="Deaths", title="Total Covid Cases and Deaths by Country")
plt.show()

covidtotals.loc[(covidtotals.total_cases<400000) \
  & (covidtotals.total_deaths>25000)].T
covidtotals.loc[(covidtotals.total_cases>700000) \
  & (covidtotals.total_deaths<25000)].T

# do a scatterplot of total_cases by total_deaths
ax = sns.regplot(x="total_cases_pm", y="total_deaths_pm", data=covidtotals)
ax.set(xlabel="Cases Per Million", ylabel="Deaths Per Million", title="Total Covid Cases per Million and Deaths per Million by Country")
plt.show()

covidtotals.loc[(covidtotals.total_cases_pm<7500) \
  & (covidtotals.total_deaths_pm>600),\
  ['location','total_cases_pm','total_deaths_pm']]
covidtotals.loc[(covidtotals.total_cases_pm>15000) \
  & (covidtotals.total_deaths_pm<=100), \
  ['location','total_cases_pm','total_deaths_pm']]







