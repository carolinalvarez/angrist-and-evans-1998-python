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
    Prepares the 1980 Census Data Extract for
    being used in empirical analysis.
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
    
    data["AGEM"]=data["AGEM"]*1
    data["AGED"]=data["AGED"]*1

    data["WEEKSM"]=data["WEEKSM"]*1
    data["WEEKSD"]=data["WEEKSD"]*1

    data["educm"] = np.where(
        ((data["FINGRADM"] == 1) | (data['FINGRADM'] == 2)), data["GRADEM"] - 2, data["GRADEM"] - 3) 
    data["educm"]=np.maximum(0, data.educm)

    data["hsgrad"]=np.where(
        (data["educm"] == 12), 1, 0) 

    data["moregrad"]=np.where(
        (data["educm"] > 12), 1, 0) 

    data["lessgrad"]=np.where(
        (data["educm"] < 12), 1, 0) 
    
    #data["total_incomed"]=(data.INCOME1D + np.maximum(0, data.INCOME2D))*2.099173554 #deflating wages as stated in Angrist and Evans (1998) 

    #data["total_incomem"]=(data.INCOME1M + np.maximum(0, data.INCOME2M))*2.099173554
    data["total_incomed"]=(data.INCOME1D + np.maximum(0, data.INCOME2D))
    data["total_incomed"]=data["total_incomed"]*2.099173554

    data["total_incomem"]=(data.INCOME1M + np.maximum(0, data.INCOME2M))
    data["total_incomem"]=data["total_incomem"]*2.099173554
    
    data["FAMINC"]=data["FAMINC"]*1
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




def data_preparation_1990(data):
    """
    Prepares the 1990 Census Data Extract for 
    being used in empirical analysis.
    """
    
    data.rename({'WEEK89D': 'WEEKSD', 
             'WEEK89M': 'WEEKSM', 
             'HOUR89M': 'HOURSM',
             'HOUR89D':'HOURSD'}, axis=1, inplace=True)
    
    data = add_constant(data, has_constant='add')

    data["boy1st"] = np.NaN
    data.loc[data.SEXK == 0, "boy1st"] = 1 #for boys
    data.loc[data.SEXK == 1, "boy1st"] = 0 #for girls

    data["boy2nd"] = np.NaN
    data.loc[data.SEX2NDK == 0, "boy2nd"] = 1 #for boys
    data.loc[data.SEX2NDK == 1, "boy2nd"] = 0 #for girls, some will have NAs because there is no second child

    data["two_boys"] = np.where(
        (data["boy1st"] == 1) & (data["boy2nd"] ==1), 1, 0)

    data["two_girls"] = np.where(
        (data["boy1st"] == 0) & (data["boy2nd"] ==0), 1, 0)

    data["same_sex"] = np.where(
        ((data["two_boys"] == 1) | (data["two_girls"] ==1)), 1, 0)

    data["mixed_sex"] = np.where(
        (((data["boy1st"] == 1) & (data["boy2nd"] ==0)) | ((data["boy1st"] == 0) & (data["boy2nd"] ==1))), 1, 0)

    data["twins"]= np.where(
        ((data["AGEK"])==(data["AGE2NDK"])), 1, 0)
    
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

    data["hsgrad"]=np.where(
        (data["YEARSCHM"] == 10), 1, 0) 

    data["moregrad"]=np.where(
        (data["YEARSCHM"] > 10), 1, 0) 

    data["lessgrad"]=np.where(
        (data["YEARSCHM"] < 10), 1, 0) 

    data["total_incomed"]=(data.INCOMED1 + np.maximum(0, data.INCOMED2))*1.238 

    data["total_incomem"]=(data.INCOMEM1 + np.maximum(0, data.INCOMEM2))*1.238 

    data["faminc"]=(data["FAMINC"])*1.238
    data["faminc_log"]=(np.log(np.maximum(data.faminc, 1)))

    data["nonmomi"]=data.faminc-(data.INCOMEM1*1.238)
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

    data["agefstm"]=data.AGEM - data.AGEK 
    data["agefstd"]=data.AGED - data.AGEK
    
    
    return data



def get_data_all_women_1980(data):
    """
    Gets samples of "All women" from 1980 PUMS extracts.
    """
    
    data_2=data[((data['AGEM']>=21) & (data['AGEM']<=35)) & (data['KIDCOUNT']>=2) & (data['AGEQ2ND']>4) & (data['agefstm']>=15) 
            & (data['ASEX']==0) & (data['AAGE']==0) & (data['AQTRBRTH']==0)  
            & (data['ASEX2ND']==0) & (data['AAGE2ND']==0) & (data['AQTRBRTH']==0)].copy()

    data_2.index = range(len(data_2.index))
    
    return data_2



def get_data_all_women_1990(data):
    """
    Gets samples of "All women" from 1990 PUMS extracts
    """
    
    data_2=data[((data['AGEM']>=21) & (data['AGEM']<=35)) & (data['KIDCOUNT']>=2) & (data['agefstm']>=15) 
            & (data['ASEX']==0) & (data['AAGE']==0) & (data['AGE2NDK']>=1)   
            & (data['ASEX2ND']==0) & (data['AAGE2ND']==0) & (data["PWGTM1"]>0)].copy()

    data_2.index = range(len(data_2.index))
    
    return data_2



def data_preparation_married_couples(data):
    """
    Gets samples of "married women" from 1980 PUMS extracts.
    """

    data["qtrmar"] = np.where((data["QTRMAR"] > 0), data["QTRMAR"] - 1, data["QTRMAR"])

    data["yom"] = np.where((data["QTRBTHM"] <= data["qtrmar"]), data["YOBM"] + data["AGEMAR"], data["YOBM"] + data["AGEMAR"]+1)


    data["dom_q"]=(data.yom + (data.qtrmar)/4)
    data["do1b_q"]=(data.YOBK + (data.QTRBKID)/4)

    data["illegit"]= np.NaN
    data.loc[data["dom_q"] - data["do1b_q"] > 0, "illegit"] = 1
    data.loc[data["dom_q"] - data["do1b_q"] <= 0, "illegit"] = 0

    bin_labels=['bottom_third', 'middle_third', 'upper_third']
    data['husband_distribution']=pd.qcut(data['total_incomed'], q=3, labels=bin_labels)

    dummies=pd.get_dummies(data["husband_distribution"]).astype(int)
    data = pd.concat([data, dummies], axis=1)

    data["more2k_lessgrad"]=data["more2k"]*data["lessgrad"]
    data["more2k_hsgrad"]=data["more2k"]*data["hsgrad"]
    data["more2k_moregrad"]=data["more2k"]*data["moregrad"]

    data["samesex_lessgrad"]=data["same_sex"]*data["lessgrad"]
    data["samesex_hsgrad"]=data["same_sex"]*data["hsgrad"]
    data["samesex_moregrad"]=data["same_sex"]*data["moregrad"]

    data["more2k_bottomthird"]=data["more2k"]*data["bottom_third"]
    data["more2k_middlethird"]=data["more2k"]*data["middle_third"]
    data["more2k_upperthird"]=data["more2k"]*data["upper_third"]

    data["samesex_bottomthird"]=data["same_sex"]*data["bottom_third"]
    data["samesex_middlethird"]=data["same_sex"]*data["middle_third"]
    data["samesex_upperthird"]=data["same_sex"]*data["upper_third"]
    
    return data


def data_preparation_married_couples_1990(data):
    """
    Gets samples of "married women" from 1990 PUMS extracts.
    """

    bin_labels=['bottom_third', 'middle_third', 'upper_third']
    data['husband_distribution']=pd.qcut(data['total_incomed'], q=3, labels=bin_labels)

    dummies=pd.get_dummies(data["husband_distribution"]).astype(int)
    data = pd.concat([data, dummies], axis=1)

    data["more2k_lessgrad"]=data["more2k"]*data["lessgrad"]
    data["more2k_hsgrad"]=data["more2k"]*data["hsgrad"]
    data["more2k_moregrad"]=data["more2k"]*data["moregrad"]

    data["samesex_lessgrad"]=data["same_sex"]*data["lessgrad"]
    data["samesex_hsgrad"]=data["same_sex"]*data["hsgrad"]
    data["samesex_moregrad"]=data["same_sex"]*data["moregrad"]

    data["more2k_bottomthird"]=data["more2k"]*data["bottom_third"]
    data["more2k_middlethird"]=data["more2k"]*data["middle_third"]
    data["more2k_upperthird"]=data["more2k"]*data["upper_third"]

    data["samesex_bottomthird"]=data["same_sex"]*data["bottom_third"]
    data["samesex_middlethird"]=data["same_sex"]*data["middle_third"]
    data["samesex_upperthird"]=data["same_sex"]*data["upper_third"]
    
    return data



def rename_interactions_earnings(data): 
    """
    Renames variables interactions for computing Table 9 and 10
    in Angrist and Evans (1998).
    """
    
    data.rename({'more2k_lessgrad': 'more2k_lessgrad_earnings', 
                                'more2k_hsgrad': 'more2k_hsgrad_earnings', 
                                'more2k_moregrad':'more2k_moregrad_earnings'}, axis=1, inplace=True)

    data.rename({'samesex_lessgrad': 'samesex_lessgrad_earnings', 
                                'samesex_hsgrad': 'samesex_hsgrad_earnings', 
                                'samesex_moregrad':'samesex_moregrad_earnings'}, axis=1, inplace=True)
    return data




def families_one_more_kid(data):
    """
    Gets samples of "families with one or more kids".
    """
    
    data_2=data[((data['AGEM']>=21) & (data['AGEM']<=35)) & (data['KIDCOUNT']>=1)].copy()
    data_2.index = range(len(data_2.index))
    
    return data_2