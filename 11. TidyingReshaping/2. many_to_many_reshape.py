# import pandas and the CMA collections data
import pandas as pd
pd.set_option('display.width', 56)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.0f}'.format
cma = pd.read_csv("data/cmacollections.csv")
cma['category'] = cma.category.str.strip().str[0:15]
cma['title'] = cma.title.str.strip().str[0:30]


# show the cma collections data

cma.shape
cma.head(4).T
cma.itemid.nunique()

cma.drop_duplicates(['itemid','citation']).\
  itemid.count()
cma.drop_duplicates(['itemid','creatorid']).\
  itemid.count()

# show a collection item with duplicated citations and creators
cma.set_index(['itemid'], inplace=True)
cma.loc[124733, ['title','citation',
  'creation_date','creator','birth_year']].head(6)

# create a collections data frame
collectionsvars = \
  ['title','category','creation_date']
cmacollections = cma[collectionsvars].\
  reset_index().\
  drop_duplicates(['itemid']).\
  set_index(['itemid'])
cmacollections.shape
cmacollections.head()
cmacollections.loc[124733]

# create a citations data frame
cmacitations = cma[['citation']].\
  reset_index().\
  drop_duplicates(['itemid','citation']).\
  set_index(['itemid'])
cmacitations.loc[124733]

# create a creators data frame
creatorsvars = \
  ['creator','birth_year','death_year']
cmacreators = cma[creatorsvars].\
  reset_index().\
  drop_duplicates(['itemid','creator']).\
  set_index(['itemid'])
cmacreators.loc[124733]

# count the number of collection items with a creator born after 1950
cmacreators['birth_year'] = \
  cmacreators.birth_year.str.\
  findall("\d+").str[0].astype(float)
youngartists = \
  cmacreators.loc[cmacreators.birth_year>1950,
  ['creator']].assign(creatorbornafter1950='Y')
youngartists.shape[0]==youngartists.index.nunique()
youngartists

cmacollections = \
  pd.merge(cmacollections, youngartists, 
  left_on=['itemid'], right_on=['itemid'], how='left')
cmacollections.creatorbornafter1950.fillna("N", inplace=True)
cmacollections.fillna({'creatorbornafter1950':'N'}, inplace=True)
cmacollections.shape
cmacollections.creatorbornafter1950.value_counts()

youngartists
