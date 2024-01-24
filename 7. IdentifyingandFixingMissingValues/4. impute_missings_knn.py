# import pandas and scikit learn's KNNImputer module
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97b.csv")
nls97.set_index("personid", inplace=True)

# prepare the NLS data

nls97['hdegnum'] = nls97.highestdegree.str[0:1].astype('float')
nls97.parentincome.replace(list(range(-5,0)), np.nan, inplace=True)

wagedatalist = ['wageincome','weeksworked16',
   'parentincome','hdegnum']
wagedata = nls97[wagedatalist]

# initialize a KNN imputation model and fill values
impKNN = KNNImputer(n_neighbors=47)
newvalues = impKNN.fit_transform(wagedata)
wagedatalistimp = ['wageincomeimp','weeksworked16imp','parentincomeimp',
  'hdegnumimp']
wagedataimp = pd.DataFrame(newvalues,
  columns=wagedatalistimp, index=wagedata.index)

# view imputed values
wagedata = wagedata.\
  join(wagedataimp[['wageincomeimp','weeksworked16imp']])
wagedata[['wageincome','wageincomeimp','weeksworked16',
  'weeksworked16imp']].head(10)

wagedata[['wageincome','wageincomeimp']].\
  agg(['count','mean','std'])

