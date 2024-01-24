# import pandas and the CMA collections data
import pandas as pd
pd.set_option('display.width', 56)
pd.set_option('display.max_columns', 6)
cmacitations = pd.read_csv("data/cmacitations.csv")
cmacreators = pd.read_csv("data/cmacreators.csv")

# look at the citations data
cmacitations['citation'] = cmacitations.citation.str[0:15]
cmacitations.head(10)
cmacitations.shape
cmacitations.id.nunique()

# look at the creators data
cmacreators['creator'] = cmacreators.creator.str[0:15]
cmacreators.loc[:,['id','creator','birth_year']].\
  head(10)
cmacreators.shape
cmacreators.id.nunique()

# show duplications of merge-by values for citations
cmacitations.id.value_counts().head(10)

# show duplications of merge-by values for creators
cmacreators.id.value_counts().head(10)

# check the merge
def checkmerge(dfleft, dfright, idvar):
  dfleft['inleft'] = "Y"
  dfright['inright'] = "Y"
  dfboth = pd.merge(dfleft[[idvar,'inleft']],\
    dfright[[idvar,'inright']], on=[idvar], how="outer")
  dfboth.fillna('N', inplace=True)
  print(pd.crosstab(dfboth.inleft, dfboth.inright))

checkmerge(cmacitations.copy(), cmacreators.copy(), "id")

# show a merge-by column duplicated in both data frames
cmacitations.loc[cmacitations.id==124733]
cmacreators.loc[cmacreators.id==124733,
  ['id','creator','birth_year','title']]

# do a many-to-many merge
cma = pd.merge(cmacitations, cmacreators, on=['id'], how="outer")
cma.loc[cma.id==124733, ['citation','creator','birth_year']]
