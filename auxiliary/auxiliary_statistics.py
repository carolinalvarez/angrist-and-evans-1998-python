"""This file contains auxiliary functions used in the main notebook for descriptive statistics and other analysis"""

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


def table_sum_stats(data):
    """
    Creates Descriptive statistics.
    """
    variables = data[
        [
            "KIDCOUNT",
            "more2k",
            "boy1st",
            "boy2nd",
            "two_boys",
            "two_girls",
            "same_sex",
            "twins",
            "AGEM",
            "agefstm",
            "workedm",
            "WEEKSM",
            "HOURSM",
            "total_incomem",
            "faminc",
            "nonmomi",
        ]
    ]

    table = pd.DataFrame()
    table["Mean"] = variables.mean()
    table["Std. Dev."] = variables.std()
    table = table.astype(float).round(3)
    table["Variable"] = [
            "Children ever born",
            "More than two children",
            "First child was a boy",
            "Second child was a boy",
            "First two children were boys",
            "First two children were girls",
            "First two children were the same sex",
            "Second birth was a twin",
            "Age",
            "Age at first birth",
            "If worked for pay in year prior to the census",
            "Weeks worked in year prior to the census",
            "Average hours worked per week",
            "Labor earnings year prior to census, 1995 dollars",
            "Family income year prior to census, 1995 dollars",
            "Non-wife income",
        
    ]
    

    return table


def table_sum_stats_husbands(data):
    """
    Creates Descriptive statistics for husbands samples.
    """
    variables = data[
        [
            "AGED",
            "agefstd",
            "workedd",
            "WEEKSD",
            "HOURSD",
            "total_incomed",
        ]
    ]

    table = pd.DataFrame()
    table["Mean"] = variables.mean()
    table["Std. Dev."] = variables.std()
    table = table.astype(float).round(3)
    table["Variable"] = [
            "Age",
            "Age at first birth",
            "If worked for pay in year prior to the census",
            "Weeks worked in year prior to the census",
            "Average hours worked per week",
            "Labor earnings year prior to census, 1995 dollars",
        
    ]
    

    return table


def Table_3_panel_1(data):
    """
    Generates the first (upper) panel of Table 3 
    from Angrist and Evans (1998).
    """
    
    variables1=["(1) one girl", "(2) one boy", "difference (2) - (1)"]
    frequencies1=['Fraction of sample', 'Fraction that had another child']
    Table_3_panel1 = pd.DataFrame(np.nan, index=variables1, columns=frequencies1)
    Table_3_panel1.index.name="Sex of first child in families with one or more children"
    a=pd.DataFrame(data['boy1st'].value_counts(normalize=True))
    a1=a.iloc[(0,0)]
    b1=a.iloc[(1,0)]

    c=pd.DataFrame(data.groupby("boy1st")["more1k"].value_counts(normalize=True))
    c1=c.iloc[(0,0)]
    d1=c.iloc[(2,0)]
    diff1=d1-c1

    Table_3_panel1.iloc[0,0]=a1
    Table_3_panel1.iloc[1,0]=b1

    Table_3_panel1.iloc[0,1]=c1
    Table_3_panel1.iloc[1,1]=d1
    Table_3_panel1.iloc[2,1]=diff1

    return Table_3_panel1


def Table_3_panel_2(data):
    """
    Generates the second (bottom) panel of Table 3 
    from Angrist and Evans (1998).
    """
    
    variables=["(1) one girl one boy", "(2) two boys", "(3) two girls", "(4) both same sex", "Difference (4) - (1)"]
    frequencies=['Fraction of sample', 'Fraction that had another child']
    Table_3_panel2 = pd.DataFrame(np.nan, index=variables, columns=frequencies)
    Table_3_panel2.index.name="Sex of first child in families with two or more children"
    a2=pd.DataFrame(data['mixed_sex'].value_counts(normalize=True))
    a2=a2.iloc[(1,0)]
    b2=pd.DataFrame(data['two_boys'].value_counts(normalize=True))
    b2=b2.iloc[(1,0)]
    c2=pd.DataFrame(data['two_girls'].value_counts(normalize=True))
    c2=c2.iloc[(1,0)]
    d2=pd.DataFrame(data['same_sex'].value_counts(normalize=True))
    d2=d2.iloc[(0,0)]

    f2=pd.DataFrame(data.groupby("mixed_sex")["more3k"].value_counts(normalize=True))
    f2=f2.iloc[(3,0)]
    g2=pd.DataFrame(data.groupby("two_boys")["more3k"].value_counts(normalize=True))
    g2=g2.iloc[(3,0)]
    h2=pd.DataFrame(data.groupby("two_girls")["more3k"].value_counts(normalize=True))
    h2=h2.iloc[(3,0)]
    i2=pd.DataFrame(data.groupby("same_sex")["more3k"].value_counts(normalize=True))
    i2=i2.iloc[(3,0)]
    diff2=(i2-f2)
    #sd_diff2=np.sum(np.square(diff2))

    Table_3_panel2.iloc[0,0]=a2
    Table_3_panel2.iloc[1,0]=b2
    Table_3_panel2.iloc[2,0]=c2
    Table_3_panel2.iloc[3,0]=d2
    Table_3_panel2.iloc[4,0]="-"
    #Table_3_panel2.iloc[5,0]="-"

    Table_3_panel2.iloc[0,1]=f2
    Table_3_panel2.iloc[1,1]=g2
    Table_3_panel2.iloc[2,1]=h2
    Table_3_panel2.iloc[3,1]=i2
    Table_3_panel2.iloc[4,1]=diff2
    #Table_3_panel2.iloc[5,1]=sd_diff2

    return Table_3_panel2




def difference_means(data, variables, instrument):
    """
    Computes difference in means between treated and 
    untreated groups by instrument.
    """
    
    table = pd.DataFrame(
        {
            "Mean difference": [],
            "Std. err.": [],
        }
    )
    
    table["demographic_vars"] = variables
    table = table.set_index("demographic_vars")
    
    for variable in variables:
        
        mean_bygroup_samesex = data.groupby(instrument)[variable].mean().to_dict()
        mean_diff_samesex = mean_bygroup_samesex[1] - mean_bygroup_samesex[0]

        std_err_samesex = np.sqrt(
            np.power(data.loc[data[instrument] == 1][variable].sem(), 2)
            + np.power(data.loc[data[instrument] == 0][variable].sem(), 2)
        )
        
        outputs = [
        mean_diff_samesex,
        std_err_samesex,

        ]
        
        table.loc[variable] = outputs
        table = table.round(4)
    
    return table
