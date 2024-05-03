# import the pandas, os, and sys libraries and load the nls and covid data
import pandas as pd
import numpy as np
import os
import sys
nls97 = pd.read_csv("data/nls97g.csv", low_memory=False)
dc = pd.read_csv("data/datacheckingtargets.csv")
dc.set_index('varname', inplace=True)

pd.set_option('display.width', 150)
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 200)

sys.path.append(os.getcwd() + "/helperfunctions")
import runchecks as rc

nls97.originalid.head(7)
nls97.loc[nls97.originalid==2,"originalid"] = 1
nls97.loc[nls97.originalid.between(3,7), "originalid"] = np.nan
nls97.originalid.head(7)
nls97["highestgradecompleted"] = nls97.highestgradecompleted.replace(95, np.nan)


dc = dc.loc[dc.include=="Y"]
numvars = dc.loc[dc.type=="numeric"].index.to_list()
catvars = dc.loc[dc.type=="categorical"].index.to_list()
idvars = dc.loc[dc.type=="unique"].index.to_list()

rc.runchecks(nls97,dc,numvars,catvars,idvars)

