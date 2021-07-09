"""This file contains auxiliary functions used in the main notebook for data preparation"""

import numpy as np
import pandas as pd
import pandas.io.formats.style
import seaborn as sns
import statsmodels as sm
import statsmodels.formula.api as smf
import statsmodels.api as sm_api
from linearmodels.iv import IV2SLS
import matplotlib as plt
import matplotlib.pyplot as plt
import copy
from IPython.display import HTML
from stargazer.stargazer import Stargazer
from statsmodels.api import add_constant
from functools import reduce


def data_preparation_1980(data):
    """
    data preparation for 1980 Census Data Extract
    """
    
    data = add_constant(data, has_constant='add')

    data["boy1st"] = np.NaN
    data.loc[data.SEXK == 0, "boy1st"] = 1 #for boys
    data.loc[data.SEXK == 1, "boy1st"] = 0 #for girls

    data["boy2nd"] = np.NaN
    data.loc[data.SEX2ND == 0, "boy2nd"] = 1 #for boys
    data.loc[data.SEX2ND == 1, "boy2nd"] = 0 #for girls, some will have NAs because there is no second child

    data["two_boys"] = np.where(
        (data["boy1st"] == 1) & (data["boy2nd"] ==1), 1, 0)

    data["two_girls"] = np.where(
        (data["boy1st"] == 0) & (data["boy2nd"] ==0), 1, 0)

    data["same_sex"] = np.where(
        ((data["two_boys"] == 1) | (data["two_girls"] ==1)), 1, 0)

    data["mixed_sex"] = np.where(
        (((data["boy1st"] == 1) & (data["boy2nd"] ==0)) | ((data["boy1st"] == 0) & (data["boy2nd"] ==1))), 1, 0)

    data["twins"]= np.where(
        ((data["AGEQ2ND"])==(data["AGEQ3RD"])), 1, 0)
    
    data["blackm"] = np.where(
        (data["RACEM"]==2), 1, 0)
    
    data["hispm"] = np.where(
        (data["RACEM"]==12), 1, 0)
    
    data["whitem"] = np.where(
        (data["RACEM"]==1), 1, 0)
    
    data["otheracem"] = np.where(
        ((data["RACEM"]!=1) & (data["hispm"] != 1) & (data["whitem"] != 1)), 1, 0)

    data["blackd"] = np.where(
        (data["RACED"]==2), 1, 0)
    
    data["hispd"] = np.where(
        (data["RACED"]==12), 1, 0)
    
    data["whited"] = np.where(
        (data["RACED"]==1), 1, 0)
    
    data["otheraced"] = np.where(
        ((data["RACED"]!=1) & (data["hispd"] != 1) & (data["whited"] != 1)), 1, 0)

    data["educm"] = np.where(
        ((data["FINGRADM"] == 1) | (data['FINGRADM'] == 2)), data["GRADEM"] - 2, data["GRADEM"] - 3) 

    data["hsgrad"]=np.where(
        (data["educm"] == 12), 1, 0) 

    data["moregrad"]=np.where(
        (data["educm"] > 12), 1, 0) 

    data["lessgrad"]=np.where(
        (data["educm"] < 12), 1, 0) 
    
    data["total_incomed"]=(data.INCOME1D + np.maximum(0, data.INCOME2D))*2.099173554 #deflating wages as stated in Angrist and Evans (1998) 

    data["total_incomem"]=(data.INCOME1M + np.maximum(0, data.INCOME2M))*2.099173554 

    data["faminc"]=data.FAMINC*2.099173554
    data["faminc_log"]=(np.log(np.maximum(data.faminc, 1)))

    data["nonmomi"]=data.faminc-(data.INCOME1M*2.099173554)
    data["nonmomi_log"]=(np.log(np.maximum(data.nonmomi, 1)))

    data["workedm"] = np.where(
        (data["WEEKSM"] > 0), 1, 0) 

    data["workedd"] = np.where(
        (data["WEEKSD"] > 0), 1, 0)
    
    data["more1k"] = np.where(
        (data["KIDCOUNT"] > 1), 1, 0) 

    data["more2k"] = np.where(
        (data["KIDCOUNT"] > 2), 1, 0) 

    data["more3k"] = np.where(
        (data["KIDCOUNT"] >= 3), 1, 0) 
    
    data["yobd"] = np.where(
        (data["QTRBTHD"] == 0), 80-data["AGED"], 79-data["AGED"]) 

    data["ageqm"]=4*(80-data.YOBM)-data.QTRBTHM-1
    data["ageqd"]=4*(80-data.yobd)-data.QTRBTHD
    data["agefstm"]=(data.ageqm-data.AGEQK)/4 
    data["agefstd"]=(data.ageqd-data.AGEQK)/4
    
    return data