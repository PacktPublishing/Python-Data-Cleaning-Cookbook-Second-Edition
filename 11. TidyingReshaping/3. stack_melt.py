# import pandas and load the nls data
import pandas as pd
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)

# view some of the weeks worked values
nls97.set_index(['originalid'], inplace=True)
weeksworkedcols = ['weeksworked17','weeksworked18',
  'weeksworked19','weeksworked20','weeksworked21']

nls97.loc[[2,3],weeksworkedcols].T
nls97.shape

# use stack to convert data from wide to long
weeksworked = nls97[weeksworkedcols].\
  stack(future_stack=True).\
  reset_index().\
  rename(columns={'level_1':'year',0:'weeksworked'})

weeksworked.loc[weeksworked.originalid.isin([2,3])]

# Fix the year values
weeksworked['year'] = \
  weeksworked.year.str[-2:].astype(int)+2000
weeksworked.loc[weeksworked.originalid.isin([2,3])]
weeksworked.shape

# use melt to transform data from wide to long
weeksworked = nls97.reset_index().\
  loc[:,['originalid'] + weeksworkedcols].\
  melt(id_vars=['originalid'],
  value_vars=weeksworkedcols,
  var_name='year', value_name='weeksworked')

weeksworked['year'] = \
  weeksworked.year.str[-2:].astype(int)+2000
weeksworked.set_index(['originalid'], inplace=True)
weeksworked.loc[[2,3]]


nls97.head(2).T

# reshape more columns with melt
colenrcols = \
  ['colenroct17','colenroct18','colenroct19',
  'colenroct20','colenroct21']
colenr = nls97.reset_index().\
  loc[:,['originalid'] + colenrcols].\
  melt(id_vars=['originalid'], value_vars=colenrcols,
    var_name='year', value_name='colenr')

colenr['year'] = colenr.year.str[-2:].astype(int)+2000
colenr.set_index(['originalid'], inplace=True)
colenr.loc[[2,3]]

# merge the weeks worked and enrollment data
workschool = \
  pd.merge(weeksworked, colenr, on=['originalid','year'], how="inner")
workschool.shape

#workschool.set_index(['originalid'], inplace=True)
workschool.loc[[2,3]]
