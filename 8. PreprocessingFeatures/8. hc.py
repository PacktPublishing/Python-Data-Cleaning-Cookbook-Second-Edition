# import pandas, numpy, and matplotlib
import pandas as pd
from feature_engine.encoding import OneHotEncoder
from category_encoders.hashing import HashingEncoder
from sklearn.model_selection import train_test_split
from feature_engine.encoding import OrdinalEncoder
from sklearn.feature_extraction import FeatureHasher
h = FeatureHasher(n_features=8, input_type='string', alternate_sign=False)
pd.set_option('display.width', 80)
pd.set_option('display.max_columns', 8)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format


covidtotals = pd.read_csv("data/covidtotals.csv")
feature_cols = ['location','population',
    'aged_65_older','diabetes_prevalence','region']
covidtotals = covidtotals[['total_cases'] + feature_cols].dropna()

# Separate into train and test sets
X_train, X_test, y_train, y_test =  \
  train_test_split(covidtotals[feature_cols],\
  covidtotals[['total_cases']], test_size=0.3, random_state=0)


oe = OrdinalEncoder(encoding_method='arbitrary', 
  variables=['region'])

X_train = oe.fit_transform(X_train)
X_train.region.value_counts().sort_index()

X_train.region

f = h.transform(X_train.region)
f.toarray()
temp = pd.DataFrame(f.toarray(), index=X_train.index) 
type(temp)
temp.shape
temp
X_train

test = pd.DataFrame({'type': ['a', 'b', 'a', 'c', 'b']})
test
f = h.transform(test.type)
f.toarray()

# use the one hot encoder for region
X_train.region.value_counts()
ohe = OneHotEncoder(top_categories=6, variables=['region'])
covidtotals_ohe = ohe.fit_transform(covidtotals)
covidtotals_ohe.filter(regex='location|region',
  axis="columns").sample(5, random_state=99).T

# use the hashing encoder for region
he = HashingEncoder(cols=['region'], n_components=6)
covidtotals_enc = he.fit_transform(covidtotals)
covidtotals_enc = covidtotals_enc.join(covidtotals[['region']])
covidtotals_enc[['col_0','col_1','col_2','col_3',
  'col_4','col_5','region']].sample(5, random_state=1)


data = pd.DataFrame([
    ['value_1', 23],
    ['value_2', 13],
    ['value_3', 42],
    ['value_4', 13],
    ['value_2', 46],
    ['value_1', 28],
    ['value_2', 32],
    ['value_3', 87],
    ['value_4', 98],
    ['value_5', 86],
    ['value_3', 45],
    ['value_2', 73],
    ['value_1', 36],
    ['value_3', 93]
], columns = ['feature1', 'feature2'])

data['feature1b'] = data.feature1

feature_hasher = FeatureHasher(n_features = 3, input_type = 'string')

temp2 = pd.DataFrame(feature_hasher.fit_transform(data['feature1']).toarray())
temp2

pd.concat([
pd.DataFrame(feature_hasher.fit_transform(data['feature1']).toarray()),
data[['feature1b','feature2']]], axis = 1)

h.fit_transform(df[['country']].to_dict(orient='records'))