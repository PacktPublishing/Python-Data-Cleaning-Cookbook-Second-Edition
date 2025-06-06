# import the pandas, os, and sys libraries
import pandas as pd
import os
import sys
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index('personid', inplace=True)

# import the basicdescriptives module
sys.path.append(os.getcwd() + "/helperfunctions")
import basicdescriptives as bd
import importlib
importlib.reload(bd)

pd.set_option('display.width', 80)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 100)
pd.options.display.float_format = '{:,.2f}'.format

# show summary statistics for continuous variables
bd.gettots(nls97[['satverbal','satmath']]).T
bd.gettots(nls97.filter(like="weeksworked"))

# count missing per column and per row
missingsbycols, missingsbyrows = \
  bd.getmissings(nls97[['weeksworked20',
  'weeksworked21']], True)
missingsbycols
missingsbyrows
missingsbycols, missingsbyrows = \
  bd.getmissings(nls97[['weeksworked20',
  'weeksworked21']])
missingsbyrows

# do frequencies for categorical columns
nls97.loc[:, nls97.dtypes == 'object'] = \
  nls97.select_dtypes(['object']). \
  apply(lambda x: x.astype('category'))
bd.makefreqs(nls97, "views/nlsfreqs.txt")

# do counts and percentages by groups
bd.getcnts(nls97, 
  ['maritalstatus','colenroct00'])
bd.getcnts(nls97, 
  ['maritalstatus','colenroct00'],
  "colenroct00.str[0:1]=='1'")
