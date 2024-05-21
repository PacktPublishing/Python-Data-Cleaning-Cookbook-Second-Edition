# import pandas and numpy, and load the nls and land temperatures data
import pandas as pd
import numpy as np
pd.set_option('display.width', 64)
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.1f}'.format
nls97 = pd.read_csv("data/nls97f.csv", low_memory=False)
nls97.set_index("personid", inplace=True)
landtemps = pd.read_csv("data/landtemps2023avgs.csv")

# use the numpy where function to create a categorical series with 2 values

landtemps.elevation.quantile(np.arange(0.2,1.1,0.2))

landtemps['elevation_group'] = np.where(landtemps.elevation>\
  landtemps.elevation.quantile(0.8),'High','Low')
landtemps.elevation_group = landtemps.elevation_group.astype('category')
landtemps.groupby(['elevation_group'], 
  observed=False)['elevation'].\
  agg(['count','min','max'])

# use the numpy where function to create a categorical series with 3 values
landtemps['elevation_group'] = \
  np.where(landtemps.elevation>
    landtemps.elevation.quantile(0.8),'High',
    np.where(landtemps.elevation>landtemps.elevation.\
      median(),'Medium','Low'))
landtemps.elevation_group = landtemps.elevation_group.astype('category')
landtemps.groupby(['elevation_group'])['elevation'].\
  agg(['count','min','max'])

# use numpy select to evaluate a list of conditions
test = [(nls97.gpaoverall<2) & 
  (nls97.highestdegree=='0. None'), 
   nls97.highestdegree=='0. None', 
   nls97.gpaoverall<2]
result = ['1. Low GPA/No Dip','2. No Diploma',
 '3. Low GPA']
nls97['hsachieve'] = np.select(test, result, '4. Did Okay')
nls97[['hsachieve','gpaoverall','highestdegree']].\
  sample(7, random_state=6)
nls97.hsachieve.value_counts().sort_index()

def gethsachieve(row):
  if (row.gpaoverall<2 and row.highestdegree=="0. None"):
    hsachieve2 = "1. Low GPA/No Dip"
  elif (row.highestdegree=="0. None"):
    hsachieve2 = "2. No Diploma"
  elif (row.gpaoverall<2):
    hsachieve2 = "3. Low GPA"
  else:
    hsachieve2 = '4. Did Okay'
  return hsachieve2

nls97['hsachieve2'] = nls97.apply(gethsachieve, axis=1)
nls97.groupby(['hsachieve','hsachieve2']).size()


# use apply and lambda to create a more complicated categorical series
def getsleepdeprivedreason(row):
  sleepdeprivedreason = "Unknown"
  if (row.nightlyhrssleep>=6):
    sleepdeprivedreason = "Not Sleep Deprived"
  elif (row.nightlyhrssleep>0):
    if (row.weeksworked20+row.weeksworked21 < 80):
      if (row.childathome>2):
        sleepdeprivedreason = "Child Rearing"
      else:
        sleepdeprivedreason = "Other Reasons"
    else:
      if (row.wageincome20>=62000 or row.highestgradecompleted>=16):
        sleepdeprivedreason = "Work Pressure"
      else:
        sleepdeprivedreason = "Income Pressure"
  else:
    sleepdeprivedreason = "Unknown"
  return sleepdeprivedreason

nls97['sleepdeprivedreason'] = nls97.apply(getsleepdeprivedreason, axis=1)
nls97.sleepdeprivedreason = nls97.sleepdeprivedreason.astype('category')
nls97.sleepdeprivedreason.value_counts()


# create a flag if individual ever had bachelor degree enrollment
nls97.loc[[999406,750699], 
  'colenrfeb00':'colenroct04'].T
nls97['baenrollment'] = nls97.filter(like="colenr").\
  transform(lambda x: x.str[0:1]=='3').\
  any(axis=1)

nls97.loc[[999406,750699], ['baenrollment']].T
nls97.baenrollment.value_counts()

