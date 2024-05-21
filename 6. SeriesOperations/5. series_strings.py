# import pandas and numpy, and load the nls and data
import pandas as pd
import numpy as np
pd.set_option('display.width', 74)
pd.set_option('display.max_columns', 8)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97ca.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# tests whether a string pattern exists in a string
nls97.govprovidejobs.value_counts()

nls97['govprovidejobsdefprob'] = \
  np.where(nls97.govprovidejobs.isnull(),
    np.nan,
      np.where(nls97.govprovidejobs.str.\
      contains("not"),"No","Yes"))
pd.crosstab(nls97.govprovidejobs, nls97.govprovidejobsdefprob)

# handle leading or trailing spaces in a string
nls97.maritalstatus.value_counts()
nls97.maritalstatus.str.startswith(' ').any()
nls97.maritalstatus.str.endswith(' ').any()
nls97['evermarried'] = \
  np.where(nls97.maritalstatus.isnull(),np.nan,
    np.where(nls97.maritalstatus.str.\
      strip()=="Never-married","No","Yes"))
pd.crosstab(nls97.maritalstatus, nls97.evermarried)

# use isin to compare a string value to a list of values
nls97['receivedba'] = \
  np.where(nls97.highestdegree.isnull(),np.nan,
    np.where(nls97.highestdegree.str[0:1].\
      isin(['4','5','6','7']),"Yes","No"))
pd.crosstab(nls97.highestdegree, nls97.receivedba)

# remove preceding numbers from highest degree values
nls97.highestdegree.value_counts(dropna=False).sort_index()
nls97.fillna({"highestdegree":"99. Unknown"},
  inplace=True)
onlytext = lambda x: x[x.find(".") + 2:]
highestdegreenonum = nls97.highestdegree.\
  astype(str).transform(onlytext)
highestdegreenonum.value_counts(dropna=False).\
  sort_index()

# use findall with a simple example
nls97.maritalstatus.head()
nls97.maritalstatus.head().str.findall("r")

pd.concat([nls97.maritalstatus.head(),
   nls97.maritalstatus.head().str.findall("r"),
   nls97.maritalstatus.head().str.findall("r").\
       str.len()],
   axis=1)

# convert a text response to numeric using numbers in the text
pd.concat([nls97.weeklyhrstv.head(),\
  nls97.weeklyhrstv.str.findall("\d+").head()], axis=1)

def getnum(numlist):
  highval = 0
  if (type(numlist) is list):
    lastval = int(numlist[-1])
    if (numlist[0]=='40'):
      highval = 45
    elif (lastval==2):
      highval = 1
    else:
      highval = lastval - 5
  else:
    highval = np.nan
  return highval

nls97['weeklyhrstvnum'] = nls97.weeklyhrstv.str.\
  findall("\d+").apply(getnum)
  
nls97[['weeklyhrstvnum','weeklyhrstv']].head(7)

pd.crosstab(nls97.weeklyhrstv, nls97.weeklyhrstvnum)


# replace values in a series with alternative values
comphrsold = ['Less than 1 hour a week',
  '1 to 3 hours a week','4 to 6 hours a week',
  '7 to 9 hours a week','10 hours or more a week']
comphrsnew = ['A. Less than 1 hour a week',
  'B. 1 to 3 hours a week','C. 4 to 6 hours a week',
  'D. 7 to 9 hours a week','E. 10 hours or more a week']
nls97.weeklyhrscomputer.value_counts().sort_index()
nls97.weeklyhrscomputer.replace(comphrsold, comphrsnew, inplace=True)
nls97.weeklyhrscomputer.value_counts().sort_index()

nls97['maritalstatus'] = nls97.maritalstatus.str.strip()
nls97.maritalstatus.value_counts(dropna=False).sort_index()
nls97.loc[nls97.maritalstatus=="Never-married"].maritalstatus.head(2).T
nls97.loc[[100284,101089],"maritalstatus"] = "Never-married "
nls97.to_csv("data/nls97ca.csv")


