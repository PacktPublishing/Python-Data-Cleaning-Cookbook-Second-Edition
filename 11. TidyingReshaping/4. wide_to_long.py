# import pandas and load the nls data
import pandas as pd
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index('personid', inplace=True)

# view some of the weeks worked and college enrollment data
weeksworkedcols = ['weeksworked17','weeksworked18',
  'weeksworked19','weeksworked20','weeksworked21']

colenrcols = ['colenroct17','colenroct18',
   'colenroct19','colenroct20','colenroct21']

nls97.loc[nls97.originalid.isin([2,3]),
  ['originalid'] + weeksworkedcols + colenrcols].T

# run the wide_to_long function
workschool = pd.wide_to_long(nls97[['originalid'] 
  + weeksworkedcols + colenrcols], 
  stubnames=['weeksworked','colenroct'], 
  i=['originalid'], j='year').reset_index()
workschool['year'] = workschool.year+2000
workschool = workschool.\
  sort_values(['originalid','year'])
workschool.set_index(['originalid'], inplace=True)
workschool.loc[[2,3]]

# run the melt with unaligned suffixes
weeksworkedcols = ['weeksworked16','weeksworked18',
  'weeksworked19','weeksworked20','weeksworked21']
workschool = pd.wide_to_long(nls97[['originalid']
  + weeksworkedcols + colenrcols], 
  stubnames=['weeksworked','colenroct'], 
  i=['originalid'], j='year').reset_index()
workschool['year'] = workschool.year+2000
workschool = workschool.sort_values(['originalid','year'])
workschool.set_index(['originalid'], inplace=True)
workschool.loc[[2,3]]

