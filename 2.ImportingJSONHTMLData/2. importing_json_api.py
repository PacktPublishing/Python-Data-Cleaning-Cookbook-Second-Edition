# import pandas, numpy, json, pprint, and requests
import pandas as pd
import json
import pprint
import requests

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 8)

# load more complicated data
response = requests.get("https://openaccess-api.clevelandart.org/api/artworks/?african_american_artists")
camcollections = json.loads(response.text)

len(camcollections['data'])
pprint.pprint(camcollections['data'][0])

# flatten the data
camcollectionsdf = \
  pd.json_normalize(camcollections['data'], 
  'citations', 
  ['accession_number','title','creation_date',
  'collection','creators','type'])
camcollectionsdf.head(2).T
creator = camcollectionsdf[:1].creators[0]
type(creator[0])
pprint.pprint(creator)

camcollectionsdf['birthyear'] = camcollectionsdf.\
 creators.apply(lambda x: x[0]['birth_year'])

camcollectionsdf.birthyear.value_counts().\
 sort_index().head()


