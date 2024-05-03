# import pandas, matplotlib, and seaborn
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.width', 53)
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97f.csv", low_memory=False)
nls97.set_index("personid", inplace=True)
covidtotals = pd.read_csv("data/covidtotals.csv", parse_dates=["lastdate"])
covidtotals.set_index("iso_code", inplace=True)

# do a boxplot for SAT verbal
nls97.satverbal.describe()

plt.boxplot(nls97.satverbal.dropna(), labels=['SAT Verbal'])
plt.annotate('outlier threshold', xy=(1.05,780), xytext=(1.15,780), size=7, arrowprops=dict(facecolor='black', headwidth=2, width=0.5, shrink=0.02))
plt.annotate('3rd quartile', xy=(1.08,570), xytext=(1.15,570), size=7, arrowprops=dict(facecolor='black', headwidth=2, width=0.5, shrink=0.02))
plt.annotate('median', xy=(1.08,500), xytext=(1.15,500), size=7, arrowprops=dict(facecolor='black', headwidth=2, width=0.5, shrink=0.02))
plt.annotate('1st quartile', xy=(1.08,430), xytext=(1.15,430), size=7, arrowprops=dict(facecolor='black', headwidth=2, width=0.5, shrink=0.02))
plt.annotate('outlier threshold', xy=(1.05,220), xytext=(1.15,220), size=7, arrowprops=dict(facecolor='black', headwidth=2, width=0.5, shrink=0.02))
plt.title("Boxplot of SAT Verbal Score")
plt.show()

# show some descriptives on weeks worked
weeksworked = nls97.loc[:, ['highestdegree',
  'weeksworked20','weeksworked21']]
weeksworked.describe()

# do a box plot of weeks worked in 2020 and 2021
plt.boxplot([weeksworked.weeksworked20.dropna(),
  weeksworked.weeksworked21.dropna()],
  labels=['Weeks Worked 2020','Weeks Worked 2021'])
plt.title("Boxplots of Weeks Worked")
plt.tight_layout()
plt.show()

# show some descriptives on coronavirus cases
totvars = ['total_cases','total_deaths',
  'total_cases_pm','total_deaths_pm']
totvarslabels = ['cases','deaths',
  'cases per million','deaths per million']
covidtotalsonly = covidtotals[totvars]
covidtotalsonly.describe()

# do a box plot of cases and deaths per million
fig, ax = plt.subplots()
plt.title("Boxplots of Covid Cases and Deaths Per Million")
ax.boxplot([covidtotalsonly.total_cases_pm,covidtotalsonly.total_deaths_pm],\
  labels=['cases per million','deaths per million'])
plt.tight_layout()
plt.show()

# show boxplots as separate sub plots on one figure
fig, axes = plt.subplots(2, 2)
fig.suptitle("Boxplots of Covid Cases and Deaths in Thousands")
axes = axes.ravel()

for j, ax in enumerate(axes):
  ax.boxplot(covidtotalsonly.iloc[:, j]/1000, labels=[totvarslabels[j]])

plt.tight_layout()
fig.subplots_adjust(top=0.9)
plt.show()

