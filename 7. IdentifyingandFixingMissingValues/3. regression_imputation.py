# import pandas
import pandas as pd
import numpy as np
import statsmodels.api as sm
pd.set_option('display.width', 74)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.2f}'.format
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# check correlations with wageincome

nls97[['wageincome20','highestdegree','weeksworked20','parentincome']].info()
nls97['hdegnum'] = nls97.highestdegree.str[0:1].astype('float')
nls97.groupby(['highestdegree','hdegnum']).size()
nls97.parentincome.replace(list(range(-5,0)), np.nan, inplace=True)
nls97[['wageincome20','hdegnum','weeksworked20','parentincome']].corr()

# check to see if folks with missing wage income data are different
# nls97.wageincome20.describe()
#nls97.loc[nls97.weeksworked20==0,'wageincome20'] = 0
nls97weeksworked = nls97.loc[nls97.weeksworked20>0]
nls97weeksworked.shape
nls97weeksworked['missingwageincome'] = \
  np.where(nls97weeksworked.wageincome20.isnull(),1,0)
nls97weeksworked.groupby(['missingwageincome'])[['hdegnum',
  'parentincome','weeksworked20']].\
  agg(['mean','count'])

# prepare data to run regression
#nls97.weeksworked20.fillna(nls97.weeksworked20.mean(), inplace=True)
nls97weeksworked.parentincome. \
  fillna(nls97weeksworked.parentincome.mean(), inplace=True)
nls97weeksworked['degltcol'] = \
  np.where(nls97weeksworked.hdegnum<=2,1,0)
nls97weeksworked['degcol'] = \
  np.where(nls97weeksworked.hdegnum.between(3,4),1,0)
nls97weeksworked['degadv'] = \
  np.where(nls97weeksworked.hdegnum>4,1,0)

# fit a linear regression model
# return the influence of each observation
# also return model coefficients
def getlm(df, ycolname, xcolnames):
  df = df[[ycolname] + xcolnames].dropna()
  y = df[ycolname]
  X = df[xcolnames]
  X = sm.add_constant(X)
  lm = sm.OLS(y, X).fit()
  coefficients = pd.DataFrame(zip(['constant'] + xcolnames,
    lm.params, lm.pvalues), columns=['features','params',
    'pvalues'])
  return coefficients, lm

#nls97 = nls97.loc[nls97.weeksworked20>0]
xvars = ['weeksworked20','parentincome','degcol','degadv']
coefficients, lm = getlm(nls97weeksworked, 'wageincome20', xvars)
coefficients

nls97weeksworked.dtypes

# generate predictions
pred = lm.predict(sm.add_constant(nls97weeksworked[xvars])).\
  to_frame().rename(columns= {0: 'pred'})
nls97weeksworked = nls97weeksworked.join(pred)

nls97weeksworked['wageincomeimp'] = \
  np.where(nls97weeksworked.wageincome20.isnull(),\
  nls97weeksworked.pred, nls97weeksworked.wageincome20)
pd.options.display.float_format = '{:,.0f}'.format
nls97weeksworked[['wageincomeimp','wageincome20'] + xvars].\
  sample(10, random_state=7)
nls97weeksworked[['wageincomeimp','wageincome20']].\
  agg(['count','mean','std'])

# add an error term
np.random.seed(0)
randomadd = np.random.normal(0, lm.resid.std(), 
   nls97weeksworked.shape[0])
randomadddf = pd.DataFrame(randomadd, columns=['randomadd'],
   index=nls97weeksworked.index)
nls97weeksworked = nls97weeksworked.join(randomadddf)
nls97weeksworked['stochasticpred'] = \
   nls97weeksworked.pred + nls97weeksworked.randomadd

nls97weeksworked['wageincomeimpstoc'] = \
  np.where(nls97weeksworked.wageincome20.isnull(),
  nls97weeksworked.stochasticpred, nls97weeksworked.wageincome20)

nls97weeksworked[['wageincomeimpstoc','wageincome20']].\
  agg(['count','mean','std'])


#nls97weeksworked = nls97weeksworked.drop(columns=['randomadd','stochasticpred','wageincomeimpstoc'], axis=1)
