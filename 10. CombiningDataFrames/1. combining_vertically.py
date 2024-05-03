# import pandas and numpy
import pandas as pd
import numpy as np
import os
pd.set_option('display.width', 58)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 50)
pd.options.display.float_format = '{:,.0f}'.format

# load the data for Cameroon and Poland
ltcameroon = pd.read_csv("data/ltcountry/ltcameroon.csv")
ltoman = pd.read_csv("data/ltcountry/ltoman.csv")

# concatenate the Cameroon and Poland data
ltcameroon.shape
ltoman.shape
ltcameroon.columns
ltoman.columns
ltcameroon.columns.\
  symmetric_difference(ltoman.columns)
ltall = pd.concat([ltcameroon, ltoman])
ltall.country.value_counts()
ltall[['country','station','temperature',
  'latitude','latabs']].\
  sample(5, random_state=3)
ltall.groupby(['country'])['latabs'].count()

# create a function to concatenate the files
def concatfiles(filelist):
  directory = "data/ltcountry/"
  ltall = pd.DataFrame()
  for filename in filelist:
    ltnew = pd.read_csv(directory + filename + ".csv")
    print(filename + " has " + 
      str(ltnew.shape[0]) + " rows.")
    ltall = pd.concat([ltall, ltnew])
  return ltall

ltall = concatfiles(['ltcameroon','ltoman'])
ltall.country.value_counts()

# concatenate all of the data files
def concatallfiles():
  directory = "data/ltcountry"
  ltall = pd.DataFrame()
  for filename in os.listdir(directory):
    if filename.endswith(".csv"): 
      fileloc = os.path.join(directory, filename)

      # open the next file
      with open(fileloc):
        ltnew = pd.read_csv(fileloc)
        print(filename + " has " + 
          str(ltnew.shape[0]) + " rows.")
        ltall = pd.concat([ltall, ltnew])

        # check for differences in columns
        columndiff = ltall.columns.\
          symmetric_difference(ltnew.columns)
        if (not columndiff.empty):
          print("", "Different column names for:",
           filename, columndiff, "", sep="\n")
          
  return ltall

ltall = concatallfiles()

ltall[['country','station','month',
 'temperature','latitude']].\
 sample(5, random_state=1)

# check values in the concatenated data
ltall.country.value_counts().sort_index()
ltall.groupby(['country']).\
  agg({'temperature':['mean','max','count'],
  'latabs':['mean','max','count']})

# fix missing values
ltall['latabs'] = np.where(ltall.country=="Oman", ltall.latitude, ltall.latabs)
ltall.groupby(['country']).\
  agg({'temperature':['mean','max','count'],
  'latabs':['mean','max','count']})
