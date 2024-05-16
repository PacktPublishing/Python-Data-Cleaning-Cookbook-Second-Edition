# import pandas, numpy, and matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.width', 65)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 20)
pd.options.display.float_format = '{:,.2f}'.format
covidtotals = pd.read_csv("data/covidtotals.csv")
covidtotals.set_index("iso_code", inplace=True)

# generate a correlation matrix of the cumulative and demographic data

covidtotals.corr(method="pearson", numeric_only=True)

# see if some countries have unexpected low or high death rates given number of cases
covidtotals['total_cases_q'] = pd.\
  qcut(covidtotals['total_cases'],
  labels=['very low','low','medium',
  'high','very high'], q=5, precision=0)

covidtotals['total_deaths_q'] = pd.\
  qcut(covidtotals['total_deaths'],
  labels=['very low','low','medium',
  'high','very high'], q=5, precision=0)

pd.crosstab(covidtotals.total_cases_q,
  covidtotals.total_deaths_q)

covidtotals.loc[(covidtotals. \
  total_cases_q=="high") & \
  (covidtotals.total_deaths_q=="low")].T

# do a scatterplot of total_cases by total_deaths
ax = sns.regplot(x=covidtotals.total_cases/1000, y=covidtotals.total_deaths)
ax.set(xlabel="Cases (thousands)", ylabel="Deaths", title="Total Covid Cases and Deaths by Country")
plt.show()

covidtotals.loc[(covidtotals.total_cases<40000000) \
  & (covidtotals.total_deaths>400000)].T
covidtotals.loc[(covidtotals.total_cases>30000000) \
  & (covidtotals.total_deaths<100000)].T

# do a scatterplot of total_cases by total_deaths
ax = sns.regplot(x="total_cases_pm", y="total_deaths_pm", data=covidtotals)
ax.set(xlabel="Cases Per Million", ylabel="Deaths Per Million", title="Total Covid Cases per Million and Deaths per Million by Country")
plt.show()



