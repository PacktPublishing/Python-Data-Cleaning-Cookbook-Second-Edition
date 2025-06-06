# import pandas, numpy, and matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.width', 80)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97f.csv", low_memory=False)
nls97.set_index("personid", inplace=True)


# do a violin plot of sat verbal scores
sns.violinplot(y=nls97.satverbal, color="wheat", orient="v")
plt.title("Violin Plot of SAT Verbal Score")
plt.ylabel("SAT Verbal")
plt.text(0.08, 780, 'outlier threshold', horizontalalignment='center', size='x-small')
plt.text(0.065, nls97.satverbal.quantile(0.75), '3rd quartile', horizontalalignment='center', size='x-small')
plt.text(0.05, nls97.satverbal.median(), 'Median', horizontalalignment='center', size='x-small')
plt.text(0.065, nls97.satverbal.quantile(0.25), '1st quartile', horizontalalignment='center', size='x-small')
plt.text(0.08, 210, 'outlier threshold', horizontalalignment='center', size='x-small')
plt.text(-0.4, 500, 'frequency', horizontalalignment='center', size='x-small')
plt.show()

# get some descriptives
nls97.loc[:, ['weeksworked20','weeksworked21']].describe()

# show weeks worked for 2020 and 2021
myplt = sns.violinplot(data=nls97.loc[:, ['weeksworked20','weeksworked21']])
myplt.set_title("Violin Plots of Weeks Worked")
myplt.set_xticklabels(["Weeks Worked 2020","Weeks Worked 2021"])
plt.show()

# do a violin plot of wage income by gender
nls97["maritalstatuscollapsed"] = \
  nls97.maritalstatus.replace(['Married',
   'Never-married','Divorced','Separated',
   'Widowed'],\
  ['Married','Never Married','Not Married',
   'Not Married','Not Married']) 
sns.violinplot(x="gender", y="wageincome20", hue="maritalstatuscollapsed",
  data=nls97, scale="count")
plt.title("Violin Plots of Wage Income by Gender and Marital Status")
plt.xlabel('Gender')
plt.ylabel('Wage Income 2020')
plt.legend(title="", loc="upper center", framealpha=0, fontsize=8)
plt.tight_layout()
plt.show()

# do a violin plot of weeks worked by degree attainment
nls97 = nls97.sort_values(['highestdegree'])
myplt = sns.violinplot(x='highestdegree',y='weeksworked21', data=nls97)
myplt.set_xticklabels(myplt.get_xticklabels(), rotation=60, horizontalalignment='right')
myplt.set_title("Violin Plots of Weeks Worked by Highest Degree")
myplt.set_xlabel('Highest Degree Attained')
myplt.set_ylabel('Weeks Worked 2021')
plt.tight_layout()
plt.show()

