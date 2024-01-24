import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.width', 53)
pd.set_option('display.max_columns', 5)


# import the land temperature data
landtemps = pd.read_csv('data/landtempssample.csv',
    names=['stationid','year','month','avgtemp','latitude',
      'longitude','elevation','station','countryid','country'],
    skiprows=1,
    parse_dates=[['month','year']])

type(landtemps)

# show enough data to get a sense of how the import went
landtemps.head(7)
landtemps.dtypes
landtemps.shape

# fix the column name for the date
landtemps.rename(columns={'month_year':'measuredate'}, inplace=True)
landtemps.dtypes
landtemps.avgtemp.describe()
landtemps.isnull().sum()

# remove rows with missing values
landtemps.dropna(subset=['avgtemp'], inplace=True)
landtemps.shape

# set data types explicitly
landtemps = pd.read_csv('data/landtempssample.csv',
    names=['stationid','year','month','avgtemp','latitude',
      'longitude','elevation','station','countryid','country'],
    skiprows=1,
    parse_dates=[['month','year']],
    dtype={'stationid':'object', 'avgtemp':'float64',
     'latitude':'float64','longitude':'float64',
     'elevation':'float64','station':'object',
     'countryid':'object','country':'object'},
    )

landtemps.info()
