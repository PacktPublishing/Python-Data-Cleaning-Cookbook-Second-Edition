# import the pandas, os, and sys libraries and load the nls and covid data
import pandas as pd
import numpy as np

def checkcats(cat1,cat2):
  missingcats = \
   set(cat1).symmetric_difference(set(cat2))
  return missingcats

def checkoutliers(values):
  thirdq, firstq = values.\
    quantile(0.75),values.\
    quantile(0.25)
  interquartilerange = 1.5*(thirdq-firstq)
  outlierhigh, outlierlow = \
    interquartilerange+thirdq, \
    firstq-interquartilerange
  return outlierhigh, outlierlow

def runchecks(df,dc,numvars,catvars,idvars):

  # check categorical variable values
  for col in df[catvars]:
    dcvals = dc.loc[col]
    print("\n\nChecks for categorical variable", col)
    compcat = list(dcvals.categories.split('|'))
    valuediff = checkcats(compcat,df[col].dropna().\
      str.strip().unique())
    if len(valuediff) > 0:
      print("at least one non-matching category:",
        valuediff)
    
    missingper = df[col].isnull().sum()/df.shape[0]
    if missingper > dcvals.missingthreshold:
      print("missing percent beyond threshold of",
      dcvals.missingthreshold, "is", missingper)

  # check numeric variable values
  for col in df[numvars]:
    dcvals = dc.loc[col]
    print("\n\nChecks for numeric variable", col)
  
    range = np.fromstring(dcvals.range, sep='|')
    min = df[col].min()
    max = df[col].max()
    if min < range[0]:
      print("at least one record below range starting at ",
       range[0], "min value is", min)

    if max > range[1]:
      print("at least one record above range ending at ", 
       range[1], "max value is", max)

    missingper = df[col].isnull().sum()/df.shape[0]
    if missingper > dcvals.missingthreshold:
      print("missing percent beyond threshold of",
       dcvals.missingthreshold, "is", missingper)
  
    if dcvals.showoutliers == "Y":
      outlierhigh, outlierlow = checkoutliers(df[col])
      print("\nvalues less than", outlierlow, "\n", 
        df.loc[df[col]<outlierlow,col].\
        agg(["min",'max','count']), end="\n")
      print("\nvalues greater than", outlierhigh,
        "\n", df.loc[df[col]>outlierhigh,col].\
        agg(["min",'max','count']), end="\n")

    skewcol = df[col].skew()

    if abs(skewcol-dcvals.skewtarget)>1.2:
      print("skew substantially different from target of",
        dcvals.skewtarget, "is", skewcol)
    
    kurtosiscol = df[col].kurtosis()
    if abs(kurtosiscol-dcvals.kurtosistarget)>1.2:
      print("kurtosis substantially different from target of",
        dcvals.kurtosistarget, "is", kurtosiscol)
    

  # check id variable values
  for col in df[idvars]:
    print("\n\nChecks for id variable", col)
  
    uniquevals = df[col].nunique()
    nrows = df.shape[0]
    if uniquevals != nrows:
      print("not unique identifier", uniquevals,
        "unique values not equal to", nrows, "rows.")
  
    missingvals = df[col].isnull().sum()
    if missingvals > 0:
      print("unique value has", missingvals,
        "missing values")
  

