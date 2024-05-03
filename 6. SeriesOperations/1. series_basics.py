# import pandas and load nls data
import pandas as pd
pd.set_option('display.width', 62)
pd.set_option('display.max_columns', 4)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.2f}'.format
nls97 = pd.read_csv("data/nls97f.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# create a series from the GPA column
gpaoverall = nls97.gpaoverall
type(gpaoverall)

gpaoverall.head()
gpaoverall.index

# select gpa values using bracket notation
gpaoverall[:5]
gpaoverall.tail()
gpaoverall[-5:]

# select values using loc
gpaoverall.loc[135335]
gpaoverall.loc[[135335]]
gpaoverall.loc[[135335,999406,151672]]
gpaoverall.loc[135335:151672]

# select values using iloc
gpaoverall.iloc[[0]]
gpaoverall.iloc[[0,1,2,3,4]]
gpaoverall.iloc[:5]
gpaoverall.iloc[-5:]

