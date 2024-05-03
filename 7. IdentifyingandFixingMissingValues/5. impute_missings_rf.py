# import pandas and scikit learn's KNNImputer module
import pandas as pd
import numpy as np
pd.options.display.float_format = '{:,.0f}'.format
from missforest.missforest import MissForest
import miceforest as mf
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# clean the NLS wage data
nls97['hdegnum'] = \
  nls97.highestdegree.str[0:1].astype('float')

nls97['parentincome'] = \
  nls97.parentincome.\
     replace(list(range(-5,0)), 
      np.nan)

# load the wage income and associated data
wagedatalist = ['wageincome20','weeksworked20','parentincome',
  'hdegnum']
wagedata = \
  nls97.loc[nls97.weeksworked20>0, wagedatalist]


# use miss forest to impute values
imputer = MissForest()
wagedataimp = imputer.fit_transform(wagedata)
wagedatalistimp = \
  ['wageincomeimp','weeksworked20imp','parentincomeimp']
wagedataimp.rename(columns=\
   {'wageincome20':'wageincome20imp',
   'weeksworked20':'weeksworked20imp',
   'parentincome':'parentincomeimp'}, inplace=True)

# view imputed values
wagedata = \
  wagedata.join(wagedataimp[['wageincome20imp',
    'weeksworked20imp']])
wagedata[['wageincome20','wageincome20imp',
  'weeksworked20','weeksworked20imp']].\
  sample(10, random_state=7)

wagedata[['wageincome20','wageincome20imp',
  'weeksworked20','weeksworked20imp']].\
  agg(['count','mean','std'])


# run miceforest instead
kernel = mf.ImputationKernel(
  data=wagedata[wagedatalist],
  save_all_iterations=True,
  random_state=1
)
kernel.mice(3,verbose=True)

wagedataimpmice = kernel.complete_data()

wagedataimpmice.rename(columns=\
  {'wageincome20':'wageincome20impmice',
  'weeksworked20':'weeksworked20impmice',
  'parentincome':'parentincomeimpmice'}, 
  inplace=True)

wagedata = wagedata[wagedatalist].\
 join(wagedataimpmice[['wageincome20impmice',
   'weeksworked20impmice']])
 
wagedata[['wageincome20','wageincome20impmice',
  'weeksworked20','weeksworked20impmice']].\
  agg(['count','mean','std'])
 
