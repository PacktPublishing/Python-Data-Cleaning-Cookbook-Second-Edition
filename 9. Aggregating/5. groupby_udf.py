# import pandas and numpy, and load the nls data
import pandas as pd
pd.set_option('display.width', 53)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.1f}'.format
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# create a function for calculating interquartile range
def iqr(x):
  return x.quantile(0.75) - x.quantile(0.25)

# run the interquartile range function
aggdict = {'weeksworked06':['count', 'mean', iqr], 'childathome':['count', 'mean', iqr]}
nls97.groupby(['highestdegree']).agg(aggdict)

# define a function to return the summary statistics as a series
def gettots(x):
  out = {}
  out['qr1'] = x.quantile(0.25)
  out['med'] = x.median()
  out['qr3'] = x.quantile(0.75)
  out['count'] = x.count()
  return out

# use apply to run the function
pd.options.display.float_format = '{:,.0f}'.format
nls97.groupby(['highestdegree'])['weeksworked06'].\
  apply(gettots)
  

# chain reset_index to set the default index
nls97.groupby(['highestdegree'])['weeksworked06'].\
  apply(gettots).reset_index()

# allow the index to be created
nlssums = nls97.groupby(['highestdegree'])\
  ['weeksworked06'].apply(gettots).unstack()
nlssums
nlssums.info()

