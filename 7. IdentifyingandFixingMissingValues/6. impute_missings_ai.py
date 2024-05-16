import pandas as pd
import numpy as np
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
llm = OpenAI(api_token="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")

pd.set_option('display.width', 72)
pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 220)
pd.options.display.float_format = '{:,.0f}'.format


# load the data frames and create a smart data frame object
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
nls97.set_index("personid", inplace=True)

# set up the degree and parent income variables

nls97['hdegnum'] = nls97.highestdegree.str[0:1].astype('category')
nls97['parentincome'] = \
  nls97.parentincome.\
  replace(list(range(-5,0)),
  np.nan)

wagedatalist = ['wageincome20','weeksworked20',
   'parentincome','hdegnum']
wagedata = nls97[wagedatalist]

wagedatasdf = SmartDataframe(wagedata, config={"llm": llm})

# show summary statistics
wagedatasdf.chat("Show the counts, means, and standard deviations as table")

# impute missings based on averages
wagedatasdf = \
  wagedatasdf.chat("Impute missing values based on average.")
  
wagedatasdf.chat("Show the counts, means, and standard deviations as table")

wagedatasdf.hdegnum.value_counts(dropna=False).sort_index()
wagedatasdf = \
  wagedatasdf.chat("Impute missings based on most frequent value")
wagedatasdf.hdegnum.value_counts(dropna=False).sort_index()

# use the impute missings function instead
wagedatasdf = SmartDataframe(wagedata, config={"llm": llm})

wagedatasdf = \
  wagedatasdf.impute_missing_values()
wagedatasdf.chat("Show the counts, means, and standard deviations as table")

# impute with knn
wagedatasdf = SmartDataframe(wagedata, config={"llm": llm})
wagedatasdf = wagedatasdf.chat("Impute missings for float variables based on knn with 47 neighbors")
wagedatasdf.chat("Show the counts, means, and standard deviations as table")

