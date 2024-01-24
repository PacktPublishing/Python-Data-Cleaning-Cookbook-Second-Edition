import pandas as pd
import numpy as np
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
llm = OpenAI(api_token="Your API token")

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 220)
pd.options.display.float_format = '{:,.0f}'.format


# load the data frames and create a smart data frame object
nls97 = pd.read_csv("data/nls97b.csv")
nls97.set_index("personid", inplace=True)

# set up the degree and parent income variables

nls97['hdegnum'] = nls97.highestdegree.str[0:1].astype('category')
nls97.parentincome.replace(list(range(-5,0)), np.nan, inplace=True)

wagedatalist = ['wageincome','weeksworked16',
   'parentincome','hdegnum']
wagedata = nls97[wagedatalist]

wagedatasdf = SmartDataframe(wagedata, config={"llm": llm})

# show summary statistics
wagedatasdf.chat("Show the counts, means, and standard deviations")

# impute missings based on averages
wagedatasdf = \
  wagedatasdf.chat("Impute missings based on average")

wagedatasdf.chat("Show the counts, means, and standard deviations")

wagedatasdf.hdegnum.value_counts(dropna=False).sort_index()
wagedatasdf = \
  wagedatasdf.chat("Impute missings based on most frequent value")
wagedatasdf.hdegnum.value_counts(dropna=False).sort_index()

# use the impute missings function instead
wagedatasdf = SmartDataframe(wagedata, config={"llm": llm})
wagedatasdf = \
  wagedatasdf.impute_missing_values()
wagedatasdf.chat("Show the counts, means, and standard deviations")

# impute with knn
wagedatasdf = SmartDataframe(wagedata, config={"llm": llm})
wagedatasdf = wagedatasdf.chat("Impute missings for float variables based on knn with 47 neighbors")
wagedatasdf.chat("Show the counts, means, and standard deviations")

# impute with random forest
wagedatasdf = SmartDataframe(wagedata, config={"llm": llm})
wagedatasdf = wagedatasdf.chat("Impute missings for float variables based on random forest")
wagedatasdf.chat("Show the counts, means, and standard deviations")

wagedatasdf.hdegnum.value_counts(dropna=False).sort_index()
