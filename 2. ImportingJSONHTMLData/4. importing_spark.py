# -*- coding: utf-8 -*-
import pandas as pd
from pyspark.sql import SparkSession

pd.set_option('display.width', 78)
pd.set_option('display.max_columns',6)

spark = SparkSession.builder \
   .getOrCreate()

landtemps = spark.read.option("header",True) \
     .csv("data/landtemps.csv")

type(landtemps)
type(spark)

landtemps.count()

landtemps.printSchema()

landtemps.select("station",'country','month','year','temp') \
    .show(5, False)

landtemps = landtemps \
  .withColumn("temp",landtemps.temp.cast('float'))

landtemps.select("temp").dtypes

landtemps.describe('temp').show()

allcandidatenews = spark.read \
     .json("data/allcandidatenewssample.json")

allcandidatenews \
  .select("source","title","story_position") \
  .show(5)

allcandidatenews.count()

allcandidatenews.printSchema()

allcandidatenews \
   .describe('story_position') \
   .show()
  
    
allcandidatenewsdf = allcandidatenews.toPandas()

allcandidatenewsdf.info()
