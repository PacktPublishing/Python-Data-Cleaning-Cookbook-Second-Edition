# import pandas, numpy, and matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
pd.set_option('display.width', 72)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
coviddaily = pd.read_csv("data/coviddaily.csv", parse_dates=["casedate"])

# look at a couple of sample rows of the covid daily data
coviddaily.sample(2, random_state=1).T

# calculate new cases and deaths by day
coviddailytotals = \
  coviddaily.loc[coviddaily.casedate.\
    between('2023-07-01','2024-03-03')].\
  groupby(['casedate'])[['new_cases','new_deaths']].\
  sum().\
  reset_index()

coviddailytotals.sample(7, random_state=1)

# show line charts for new cases and new deaths by day
fig = plt.figure()
plt.suptitle("New Covid Cases and Deaths By Day Worldwide 2023-2024")
ax1 = plt.subplot(2,1,1)
ax1.plot(coviddailytotals.casedate, coviddailytotals.new_cases)
ax1.xaxis.set_major_formatter(DateFormatter("%b"))
ax1.set_xlabel("New Cases")
ax2 = plt.subplot(2,1,2)
ax2.plot(coviddailytotals.casedate, coviddailytotals.new_deaths)
ax2.xaxis.set_major_formatter(DateFormatter("%b"))
ax2.set_xlabel("New Deaths")
plt.tight_layout()
fig.subplots_adjust(top=0.88)
plt.show()

# calculate new cases and new deaths by region and day
regiontotals = \
  coviddaily.loc[coviddaily.casedate.\
    between('2023-07-01','2024-03-03')].\
  groupby(['casedate','region'])\
    [['new_cases','new_deaths']].\
  sum().\
  reset_index()

regiontotals.sample(7, random_state=1)

# show plot of new cases by selected regions
showregions = ['East Asia','Southern Africa',
  'North America','Western Europe']

for j in range(len(showregions)):
  rt = regiontotals.loc[regiontotals.\
    region==showregions[j],
    ['casedate','new_cases']]
  plt.plot(rt.casedate, rt.new_cases,
    label=showregions[j])

plt.title("New Covid Cases By Day and Region in 2023-2024")
plt.gca().get_xaxis().set_major_formatter(DateFormatter("%b"))
plt.ylabel("New Cases")
plt.legend()
plt.show()

sa = \
  coviddaily.loc[(coviddaily.casedate.\
    between('2023-01-01','2023-10-31')) & \
    (coviddaily.region=='South America'),
    ['casedate','new_cases']].\
  groupby(['casedate'])\
    [['new_cases']].\
  sum().\
  reset_index().\
  rename(columns={'new_cases':'sacases'})
  
br = coviddaily.loc[(coviddaily.\
  location=='Brazil') & \
  (coviddaily.casedate. \
  between('2023-01-01','2023-10-31')),
  ['casedate','new_cases']].\
  rename(columns={'new_cases':'brcases'})
sa = pd.merge(sa, br, left_on=['casedate'], right_on=['casedate'], how="left")
sa.fillna({"sacases": 0}, 
  inplace=True)
sa['sacasesnobr'] = sa.sacases-sa.brcases
#saabb = sa.loc[sa.casedate.between('2023-01-01','2023-10-01')]

fig = plt.figure()
ax = plt.subplot()
ax.stackplot(sa.casedate, sa.sacases, sa.sacasesnobr, labels=['Brazil','Other South America'])
ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))
plt.title("New Covid Cases in South America in 2023")
plt.tight_layout()
plt.legend(loc="upper left")
plt.show()
