# import pandas, numpy, json, pprint, and requests
import pandas as pd
import pprint
import requests
from bs4 import BeautifulSoup

pd.set_option('display.width', 85)
pd.set_option('display.max_columns',8)

# parse the web page and get the header row of the table

webpage = requests.get("http://www.alrb.org/datacleaning/highlowcases.html")

bs = BeautifulSoup(webpage.text, 'html.parser')
theadrows = bs.find('table', {'id':'tblLowCases'}).thead.find_all('th')
type(theadrows)
labelcols = [j.get_text() for j in theadrows]
labelcols[0] = "rowheadings"
labelcols

# get the data from the table cells
rows = bs.find('table', {'id':'tblLowCases'}).tbody.find_all('tr')
datarows = []
labelrows = []
for row in rows:
  rowlabels = row.find('th').get_text()
  cells = row.find_all('td', {'class':'data'})
  if (len(rowlabels)>3):
    labelrows.append(rowlabels)
  if (len(cells)>0):
    cellvalues = [j.get_text() for j in cells]
    datarows.append(cellvalues)

pprint.pprint(datarows[0:2])
pprint.pprint(labelrows[0:2])

for i in range(len(datarows)):
  datarows[i].insert(0, labelrows[i])

pprint.pprint(datarows[0:2])

labelcols

# load the data into pandas
lowcases = pd.DataFrame(datarows, columns=labelcols)
lowcases.iloc[:,1:5].head()
lowcases.dtypes
lowcases.columns = lowcases.columns.str.replace(" ", "_").str.lower()

#lowcases.columns
#fixcols = ['total_cases','total_deaths','total_cases_pm','total_deaths_pm','population','gdp_per_capita']

for col in lowcases.columns[2:-1]:
  lowcases[col] = lowcases[col].\
    str.replace("[^0-9]","",regex=True).astype('int64')

lowcases['last_date'] = pd.to_datetime(lowcases.last_date)
lowcases['median_age'] = lowcases['median_age'].astype('float')

lowcases.dtypes

