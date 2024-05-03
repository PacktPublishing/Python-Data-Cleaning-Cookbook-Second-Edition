import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
llm = OpenAI(api_token="Your API key")

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 220)
pd.options.display.float_format = '{:,.0f}'.format

# load the data frames and create a smart data frame object
covidcases = pd.read_csv("data/covidcases.csv")

nls97 = pd.read_csv("data/nls97f.csv", low_memory=False)
nls97.set_index("personid", inplace=True)
nls97sdf = SmartDataframe(nls97, config={"llm": llm})

# run some queries
nls97sdf.chat("Show average of gpaoverall")
nls97sdf.chat("Show average for each weeks worked columns")
nls97sdf.chat("Show satmath average by gender")


nls97sdf = nls97sdf.chat("Set childnum to child at home plus child not at home")
nls97sdf[['childnum','childathome','childnotathome']].\
  sample(5, random_state=1)

nls97sdf = nls97sdf.chat("evermarried is 'No' when maritalstatus is 'Never-married', else 'Yes'")
nls97sdf.groupby(['evermarried','maritalstatus']).size()

nls97sdf = nls97sdf.chat("if maritalstatus is ‘Never-married’ set evermarried2 to 'No', otherwise 'Yes'")
nls97sdf.groupby(['evermarried2','maritalstatus']).size()
nls97sdf.head(2).T

nls97sdf = nls97sdf.chat("set weeksworkedavg to the average for weeksworked columns")
nls97sdf

nls97sdf.gpaenglish.describe()
nls97sdf = nls97sdf.chat("set missing gpaenglish to the average")
nls97sdf.gpaenglish.describe()


# calculate days since first case by country
firstcase = covidcases.\
  sort_values(['location','casedate']).\
  drop_duplicates(['location'], keep='first')

firstcase.set_index('location', inplace=True)

firstcase.shape

firstcase[['iso_code','continent','casedate',
  'total_cases','new_cases']].head(2).T

# try it with a pandasai smart data frame
covidcasessdf = SmartDataframe(covidcases, config={"llm": llm})

firstcasesdf = covidcasessdf.chat("Show first casedate and location and other values for each country.")
firstcasesdf.info()
firstcasesdf.shape
#firstcasesdf = firstcasesdf.chat("Make location the index.")
firstcasesdf[['location','continent','casedate',
  'total_cases','new_cases']].head(2).T


