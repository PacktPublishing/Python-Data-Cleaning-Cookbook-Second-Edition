# import pandas and scikit learn's KNNImputer module
import pandas as pd
import numpy as np
pd.options.display.float_format = '{:,.1f}'.format
from missforest.missforest import MissForest
import miceforest as mf
nls97 = pd.read_csv("data/nls97b.csv")
nls97.set_index("personid", inplace=True)

# clean the NLS wage data
nls97['hdegnum'] = nls97.highestdegree.str[0:1].astype('float')
nls97.parentincome.replace(list(range(-5,0)), np.nan, inplace=True)

# load the wage income and associated data
wagedatalist = ['wageincome','weeksworked16','parentincome',
  'hdegnum']
wagedata = nls97[wagedatalist]

# use miss forest to impute values
imputer = MissForest()
wagedataimp = imputer.fit_transform(wagedata)
wagedatalistimp = ['wageincomeimp','weeksworked16imp','parentincomeimp']
wagedataimp.rename(columns={'wageincome':'wageincomeimp',
   'weeksworked16':'weeksworked16imp','parentincome':'parentincomeimp'},
      inplace=True)


# view imputed values
wagedata = wagedata.join(wagedataimp[['wageincomeimp','weeksworked16imp']])
wagedata[['wageincome','wageincomeimp','weeksworked16',
  'weeksworked16imp']].head(10)

wagedata[['wageincome','wageincomeimp','weeksworked16','weeksworked16imp']].\
  agg(['count','mean','std'])


# run miceforest instead
kernel = mf.ImputationKernel(
  data=wagedata,
  save_all_iterations=True,
  random_state=1
)
kernel.mice(3,verbose=True)

wagedataimpmice = kernel.complete_data()

wagedataimpmice.rename(columns={'wageincome':'wageincomeimpmice',
   'weeksworked16':'weeksworked16impmice','parentincome':\
      'parentincomeimpmice'}, inplace=True)

wagedata = wagedata.\
 join(wagedataimpmice[['wageincomeimpmice','weeksworked16impmice']])
 
wagedata[['wageincome','wageincomeimpmice','weeksworked16','weeksworked16impmice']].\
  agg(['count','mean','std'])
 
