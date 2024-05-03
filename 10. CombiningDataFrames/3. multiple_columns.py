# import pandas, and load the nls weeks worked and college data
import pandas as pd
pd.set_option('display.width', 68)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 100)
pd.options.display.float_format = '{:,.0f}'.format
nls97weeksworked = pd.read_csv("data/nls97weeksworked.csv")
nls97colenr = pd.read_csv("data/nls97colenr.csv")

# look at some of the nls data
nls97weeksworked.loc[nls97weeksworked.\
  originalid.isin([2,3])]
    
nls97weeksworked.shape

nls97weeksworked.originalid.nunique()
nls97colenr.loc[nls97colenr.\
  originalid.isin([2,3])]

nls97colenr.shape
nls97colenr.originalid.nunique()

# check for unique ids
nls97weeksworked.groupby(['originalid','year'])\
  ['originalid'].count().shape
nls97colenr.groupby(['originalid','year'])\
  ['originalid'].count().shape

# create a function to check id mismatches
def checkmerge(dfleft, dfright, idvar):
  dfleft['inleft'] = "Y"
  dfright['inright'] = "Y"
  dfboth = pd.merge(dfleft[idvar + ['inleft']],\
    dfright[idvar + ['inright']], on=idvar, how="outer")
  dfboth.fillna('N', inplace=True)
  print(pd.crosstab(dfboth.inleft, dfboth.inright))

checkmerge(nls97weeksworked.copy(),nls97colenr.copy(), ['originalid','year'])

# use multiple merge-by columns
nls97workschool = \
  pd.merge(nls97weeksworked, nls97colenr,
  on=['originalid','year'], how="inner")
nls97workschool.shape
nls97workschool.loc[nls97workschool.\
  originalid.isin([2,3])]
