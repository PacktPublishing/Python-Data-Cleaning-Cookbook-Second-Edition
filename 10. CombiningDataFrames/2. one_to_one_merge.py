# import pandas and numpy, and load the nls data
import pandas as pd
pd.set_option('display.width', 52)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97f.csv", low_memory=False)
nls97.set_index("personid", inplace=True)
nls97add = pd.read_csv("data/nls97add.csv")

# look at some of the nls data
nls97.head()

nls97.shape
nls97add.head()
nls97add.shape

# check for unique ids
nls97.originalid.nunique()==nls97.shape[0]
nls97add.originalid.nunique()==nls97add.shape[0]

# create some mismatched ids
nls97 = nls97.sort_values('originalid')
nls97add = nls97add.sort_values('originalid')
nls97.loc[[135335,999406], "originalid"] = \
  nls97.originalid+10000
nls97.originalid.head(2)
nls97add.loc[[0,1], "originalid"] = \
  nls97add.originalid+20000
nls97add.originalid.head(2)
nls97.set_index("originalid", inplace=True)
nls97add.set_index("originalid", inplace=True)


# use join to do a left join
nlsnew = nls97.join(nls97add)
nlsnew.loc[nlsnew.index>9999, ['gender','birthyear','motherage','parentincome']]

# do a left join with merge
nlsnew = pd.merge(nls97, nls97add, on=['originalid'], how="left")
nlsnew.loc[nlsnew.index>9999, ['gender','birthyear','motherage','parentincome']]

# do a right join
nlsnew = pd.merge(nls97, nls97add, on=['originalid'], how="right")
nlsnew.loc[nlsnew.index>9999, ['gender','birthyear','motherage','parentincome']]

# do an inner join
nlsnew = pd.merge(nls97, nls97add, on=['originalid'], how="inner")
nlsnew.loc[nlsnew.index>9999, ['gender','birthyear','motherage','parentincome']]

# do an outer join
nlsnew = pd.merge(nls97, nls97add, on=['originalid'], how="outer")
nlsnew.loc[nlsnew.index>9999, ['gender','birthyear','motherage','parentincome']]

# create a function to check id mismatches
def checkmerge(dfleft, dfright, idvar):
  dfleft['inleft'] = "Y"
  dfright['inright'] = "Y"
  dfboth = pd.merge(dfleft[[idvar,'inleft']],\
    dfright[[idvar,'inright']], on=[idvar], how="outer")
  dfboth.fillna('N', inplace=True)
  print(pd.crosstab(dfboth.inleft, dfboth.inright))

checkmerge(nls97.reset_index(),nls97add.reset_index(), "originalid")



nlsnew = pd.merge(nls97, nls97add, left_on=['originalid'], right_on=['originalid'], how="right")
nlsnew.loc[nlsnew.index>9999, ['gender','birthyear','motherage','parentincome']]
