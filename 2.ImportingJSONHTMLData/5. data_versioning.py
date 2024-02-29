# -*- coding: utf-8 -*-
import pandas as pd
from deltalake.writer import write_deltalake
from deltalake import DeltaTable
import os

pd.set_option('display.width', 78)
pd.set_option('display.max_columns',6)

os.makedirs("data/temps_lake", exist_ok=True)

landtemps = pd.read_csv('data/landtempssample.csv',
    names=['stationid','year','month','avgtemp','latitude',
      'longitude','elevation','station','countryid','country'],
    skiprows=1,
    parse_dates=[['month','year']])

landtemps.shape

write_deltalake("data/temps_lake", landtemps)

tempsdelta = DeltaTable("data/temps_lake", version=0)
type(tempsdelta)
tempsdfv1 = tempsdelta.to_pandas()
tempsdfv1.shape

write_deltalake("data/temps_lake", landtemps.head(1000), mode="overwrite")

tempsdfv2 = DeltaTable("data/temps_lake", version=1).to_pandas()
tempsdfv2.shape

write_deltalake("data/temps_lake", landtemps.head(1000), mode="append")

tempsdfv3 = DeltaTable("data/temps_lake", version=2).to_pandas()
tempsdfv3.shape

DeltaTable("data/temps_lake", version=0).to_pandas().shape
