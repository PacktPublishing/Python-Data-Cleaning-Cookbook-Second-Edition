# import pandas
import pandas as pd
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 12)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# set up school record and demographic data frames from the NLS data
schoolrecordlist = ['satverbal','satmath','gpaoverall',
  'gpaenglish',  'gpamath','gpascience','highestdegree',
  'highestgradecompleted']

schoolrecord = nls97[schoolrecordlist]
schoolrecord.shape

# check the school record data for missings
schoolrecord.isnull().sum(axis=0)
misscnt = schoolrecord.isnull().sum(axis=1)
misscnt.value_counts().sort_index()
schoolrecord.loc[misscnt>=7].head(4).T

# remove rows with almost all missing data
schoolrecord = schoolrecord.dropna(thresh=2)
schoolrecord.shape
schoolrecord.isnull().sum(axis=1).value_counts().sort_index()

# assign mean values to missings
schoolrecord = nls97[schoolrecordlist]
schoolrecord.gpaoverall.agg(['mean','std','count'])
schoolrecord.fillna({"gpaoverall":\
 schoolrecord.gpaoverall.mean()}, 
 inplace=True)
schoolrecord.gpaoverall.isnull().sum()
schoolrecord.gpaoverall.agg(['mean','std','count'])

# use forward fill
wageincome20 = nls97.wageincome20.copy(deep=True)
wageincome20.isnull().sum()

# wageincome.agg(['mean','std','count'])
wageincome20.head().T
wageincome20.ffill(inplace=True)
wageincome20.head().T
wageincome20.isnull().sum()
# wageincome.agg(['mean','std','count'])

wageincome20 = nls97.wageincome20.copy(deep=True)
wageincome20.head().T
wageincome20.std()
wageincome20.bfill(inplace=True)
wageincome20.head().T
wageincome20.std()


# fill missings with the average by group
nls97.weeksworked20.mean()
nls97.groupby(['highestdegree'])['weeksworked20'].mean()

nls97.loc[nls97.highestdegree.notnull(), 'weeksworked20imp'] = \
  nls97.loc[nls97.highestdegree.notnull()].\
  groupby(['highestdegree'])['weeksworked20'].\
  transform(lambda x: x.fillna(x.mean()))

nls97[['weeksworked20imp','weeksworked20','highestdegree']].\
  head(10)
nls97[['weeksworked20imp','weeksworked20']].\
  agg(['mean','count'])


