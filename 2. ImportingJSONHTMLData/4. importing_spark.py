# -*- coding: utf-8 -*-
import pandas as pd
from pyspark.sql import SparkSession

pd.set_option('display.width', 78)
pd.set_option('display.max_columns',6)

# initiate a Spark session and import CSV data
spark = SparkSession.builder \
   .getOrCreate()

landtemps = spark.read.option("header",True) \
     .csv("data/landtemps.csv")

type(landtemps)
type(spark)

# look at the structure of the Spark DataFrame
landtemps.count()

landtemps.printSchema()

landtemps.select("station",'country','month','year','temp') \
    .show(5, False)

# chagne a data type
landtemps = landtemps \
  .withColumn("temp",landtemps.temp.cast('float'))

landtemps.select("temp").dtypes

landtemps.describe('temp').show()

# load JSON data
allcandidatenews = spark.read \
     .json("data/allcandidatenewssample.json")

allcandidatenews \
  .select("source","title","story_position") \
  .show(5)

# look at the structure of the JSON data
allcandidatenews.count()

allcandidatenews.printSchema()

allcandidatenews \
   .describe('story_position') \
   .show()
  
    
allcandidatenewsdf = allcandidatenews.toPandas()

allcandidatenewsdf.info()
