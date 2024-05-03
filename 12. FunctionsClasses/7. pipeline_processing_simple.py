# import pandas, numpy, and matplotlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold

pd.set_option('display.width', 150)
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 100)
pd.options.display.float_format = '{:,.3f}'.format

# load the NLS data
landtemps = pd.read_csv("data/landtemps2023avgs.csv")

feature_cols = ['latabs','elevation']

X_train, X_test, y_train, y_test =  \
  train_test_split(landtemps[feature_cols],\
  landtemps[['avgtemp']], test_size=0.1, random_state=0)

kf = KFold(n_splits=5, shuffle=True, random_state=0)
type(kf)
      
pipeline = \
  make_pipeline(StandardScaler(),
  SimpleImputer(strategy="mean"),LinearRegression())

scores = \
  cross_validate(pipeline, X=X_train, y=y_train.values,
  cv=kf, scoring=['r2','neg_mean_absolute_error'], 
  n_jobs=1)

print("Mean Absolute Error: %.2f, R-squared: %.2f" % 
  (scores['test_neg_mean_absolute_error'].mean(),
  scores['test_r2'].mean()))

