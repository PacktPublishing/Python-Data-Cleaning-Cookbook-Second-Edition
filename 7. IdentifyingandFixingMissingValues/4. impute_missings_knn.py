# import pandas and scikit learn's KNNImputer module
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
pd.set_option('display.width', 74)
pd.set_option('display.max_columns', 8)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# prepare the NLS data

nls97['hdegnum'] = \
  nls97.highestdegree.str[0:1].astype('float')
nls97['parentincome'] = \
  nls97.parentincome.\
     replace(list(range(-5,0)), 
      np.nan)

wagedatalist = ['wageincome20','weeksworked20',
   'parentincome','hdegnum']
wagedata = \
  nls97.loc[nls97.weeksworked20>0, wagedatalist]
wagedata.shape

# initialize a KNN imputation model and fill values
impKNN = KNNImputer(n_neighbors=38)
newvalues = impKNN.fit_transform(wagedata)
wagedatalistimp = ['wageincomeimp','weeksworked20imp',
  'parentincomeimp','hdegnumimp']
wagedataimp = pd.DataFrame(newvalues,
  columns=wagedatalistimp, index=wagedata.index)

# view imputed values
wagedata = wagedata.\
  join(wagedataimp[['wageincomeimp','weeksworked20imp']])
wagedata[['wageincome20','wageincomeimp','weeksworked20',
  'weeksworked20imp']].sample(10, random_state=7)

wagedata[['wageincome20','wageincomeimp']].\
  agg(['count','mean','std'])

wagedata[['wageincome20','wageincomeimp','weeksworked20',
  'weeksworked20imp']].sample(10, random_state=1)
