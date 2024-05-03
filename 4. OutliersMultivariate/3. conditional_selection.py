# import pandas, numpy, and matplotlib
import pandas as pd
pd.set_option('display.width', 55)
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 100)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97f.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# look at some of the nls data
nls97[['wageincome20','highestgradecompleted',
  'highestdegree']].head(3).T

nls97.dtypes

nls97.loc[:, "weeksworked18":"weeksworked22"].head(3).T
nls97.loc[:, "colenroct15":"colenrfeb22"].head(2).T

# show individuals with wage income but no weeks worked
nls97.loc[(nls97.weeksworked20==0) &
   nls97.wageincome20>0, 
  ['weeksworked20','wageincome20']]

# check for ever enrolled in 4-year college
nls97.filter(like="colenr").\
  apply(lambda x: x.str[0:1]=='3').\
  head(2).T
nls97.filter(like="colenr").\
  apply(lambda x: x.str[0:1]=='3').\
  any(axis=1).head(2)

# show individuals with post-graduate enrollment but no bachelor's enrollment
nobach = nls97.loc[nls97.filter(like="colenr").\
  apply(lambda x: x.str[0:1]=='4').\
  any(axis=1) & ~nls97.filter(like="colenr").\
  apply(lambda x: x.str[0:1]=='3').\
  any(axis=1), "colenrfeb97":"colenrfeb22"]
len(nobach)
nobach.head(2).T

# show individuals with bachelor's degrees or more but no 4-year college enrollment
nls97.highestdegree.value_counts().sort_index()
no4yearenrollment = \
  nls97.loc[nls97.highestdegree.str[0:1].\
  isin(['4','5','6','7']) & \
  ~nls97.filter(like="colenr").\
  apply(lambda x: x.str[0:1]=='3').\
  any(axis=1), "colenrfeb97":"colenrfeb22"]
len(no4yearenrollment)
no4yearenrollment.head(2).T

# show individuals with wage income more than three standard deviations greater than or less than the mean
highwages = \
 nls97.loc[nls97.wageincome20 > 
 nls97.wageincome20.mean()+ \
 (nls97.wageincome20.std()*3),
 ['wageincome20']]
highwages

# show individuals with large changes in weeks worked in the most recent year
workchanges = nls97.loc[~nls97.loc[:,
  "weeksworked16":"weeksworked20"].mean(axis=1).\
  between(nls97.weeksworked21*0.5,\
  nls97.weeksworked21*2) \
  & ~nls97.weeksworked21.isnull(), 
  "weeksworked16":"weeksworked21"]
len(workchanges)
workchanges.head(6).T

# show inconsistencies between highest grade completed and highest degree
ltgrade12 = nls97.loc[nls97.highestgradecompleted<12, ['highestgradecompleted','highestdegree']]
pd.crosstab(ltgrade12.highestgradecompleted, ltgrade12.highestdegree)

