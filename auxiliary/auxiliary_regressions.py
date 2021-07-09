"""This file contains auxiliary functions used in the main notebook for regression results"""


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


def OLS_Regressions_more2k(data1, data2):
    
    model1_table6=sm_api.OLS(data1["more2k"], sm_api.add_constant(data1["same_sex"])).fit()
    model2_table6=sm_api.OLS(data1["more2k"], sm_api.add_constant(data1[["same_sex", "boy1st", "boy2nd", "AGEM", 'agefstm', "blackm", "hispm",     "otheracem"]])).fit()
    model3_table6=sm_api.OLS(data1["more2k"], sm_api.add_constant(data1[["boy1st", "two_boys", "two_girls", "AGEM", 'agefstm', "blackm",           "hispm", "otheracem"]])).fit()
    model4_table6=sm_api.OLS(data2["more2k"], sm_api.add_constant(data2["same_sex"])).fit()
    model5_table6=sm_api.OLS(data2["more2k"], sm_api.add_constant(data2[["same_sex", "boy1st", "boy2nd", "AGEM", 'agefstm', "blackm", "hispm",     "otheracem"]])).fit()
    model6_table6=sm_api.OLS(data2["more2k"], sm_api.add_constant(data2[["boy1st", "two_boys", "two_girls", "AGEM", 'agefstm', "blackm",           "hispm", "otheracem"]])).fit()
    Table = Stargazer([model1_table6, model2_table6, model3_table6, model4_table6, model5_table6, model6_table6])

    Table.custom_columns(['All women', 'All women', 'All women', 'Married women', 'Married women', 'Married women'], 
                         [1, 1, 1, 1, 1, 1])
    Table.significant_digits(4)
    
    return Table



def OLS_Labor_Supply_Models(data, outcomes, controls_1, controls_2, controls_3):

    table = pd.DataFrame(
        {
            "OLS (1)": [],
            "Std.err (1)": [],
            "IV-same sex (2)": [],
            "Std.err (2)": [],
            "IV-two girls, two boys (3)": [],
            "Std.err (3)": [],
        }
    )
    table["outcomes"] = outcomes
    table = table.set_index("outcomes")

    for outcome in outcomes:

        data=data
        model_OLS=sm_api.OLS(data[outcome], (data[controls_1]))
        result_OLS=model_OLS.fit()
        model_IV_1=IV2SLS(data[outcome], data[controls_2], data["more2k"], data["same_sex"])
        result_IV_1=model_IV_1.fit()
        model_IV_2=IV2SLS(data[outcome], data[controls_3], data["more2k"], data[["two_boys","two_girls"]])
        result_IV_2=model_IV_2.fit()        
        
        outputs = [
                result_OLS.params["more2k"],
                result_OLS.bse["more2k"],
                result_IV_1.params["more2k"],
                result_IV_1.std_errors["more2k"],
                result_IV_2.params["more2k"],
                result_IV_2.std_errors["more2k"],
            
        ]
        
        table.loc[outcome] = outputs
        table = table.round(3)

    return table



def OLS_Labor_Supply_Interactions_wifes(data, Interaction, outcome):
    
    table = pd.DataFrame(
        {
            "OLS (1)": [],
            "Std.err (1)": [],

        }
    )
    table["Interactions"] = Interaction
    table = table.set_index("Interactions")
    table

    for interaction in Interaction:

        mod=sm_api.OLS(data[outcome], data[[interaction, "more2k", "AGEM", "agefstm", "boy1st", "boy2nd", "blackm", "hispm", "otheracem"]])
        results_mod=mod.fit()


        outputs = [
                results_mod.params["more2k"],
                results_mod.bse["more2k"],
        ]

        table.loc[interaction] = outputs

    return table



def OLS_Labor_Supply_Interactions_husbands(data1, data2, data3, Interaction, outcome):
    
    table = pd.DataFrame(
        {
            "OLS (1)": [],
            "Std.err (1)": [],

        }
    )
    table["Interactions"] = Interaction
    table = table.set_index("Interactions")
    table
    
    
    mod1=sm_api.OLS(data1[outcome], data1[["const", "more2k", "AGED", "agefstd", "boy1st", "boy2nd", "blackd", "hispd", "otheraced"]])
    results_mod1=mod1.fit()
    
    mod2=sm_api.OLS(data2[outcome], data2[["const", "more2k", "AGED", "agefstd", "boy1st", "boy2nd", "blackd", "hispd", "otheraced"]])
    results_mod2=mod2.fit()

    mod3=sm_api.OLS(data3[outcome], data3[["const", "more2k", "AGED", "agefstd", "boy1st", "boy2nd", "blackd", "hispd", "otheraced"]])
    results_mod3=mod3.fit()


    outputs1 = [results_mod1.params["more2k"], results_mod1.bse["more2k"],]
    outputs2 = [results_mod2.params["more2k"], results_mod2.bse["more2k"],]
    outputs3 = [results_mod3.params["more2k"], results_mod3.bse["more2k"],]

    table.loc["more2k_lessgrad_husbands"] = outputs1
    table.loc["more2k_hsgrad_husbands"] = outputs2
    table.loc["more2k_moregrad_husbands"] = outputs3

    return table


def OLS_Labor_Supply_First_Stage_wifes(data, Interaction, outcome):
    
    table = pd.DataFrame(
        {
            "OLS (1)": [],
            "Std.err (1)": [],

        }
    )
    table["Interactions"] = Interaction
    table = table.set_index("Interactions")
    table

    for interaction in Interaction:

        mod=sm_api.OLS(data[outcome], data[[interaction, "same_sex", "AGEM", "agefstm", "boy1st", "boy2nd", "blackm", "hispm", "otheracem"]])
        results_mod=mod.fit()


        outputs = [
                results_mod.params["same_sex"],
                results_mod.bse["same_sex"],
        ]

        table.loc[interaction] = outputs

    return table




def OLS_Labor_Supply_First_Stage_husbands(data, Interaction, outcome):
    
    table = pd.DataFrame(
        {
            "OLS (1)": [],
            "Std.err (1)": [],

        }
    )
    table["Interactions"] = Interaction
    table = table.set_index("Interactions")
    table

    for interaction in Interaction:

        mod=sm_api.OLS(data[outcome], data[[interaction, "same_sex", "AGED", "agefstd", "boy1st", "boy2nd", "blackd", "hispd", "otheraced"]])
        results_mod=mod.fit()


        outputs = [
                results_mod.params["same_sex"],
                results_mod.bse["same_sex"],
        ]

        table.loc[interaction] = outputs

    return table


def IV_Labor_Supply_Interactions(data, data2, data3, data4, data5, outcome, outcome2):
    
    table = pd.DataFrame(
        {
            "IV (2)": [],
            "Std.err (2)": [],

        }
    )
    table["Interactions"] = [
        "more2k_bottomthird", 
        "more2k_middlethird", 
        "more2k_upperthird", 
        "more2k_lessgrad", 
        "more2k_hsgrad", 
        "more2k_moregrad",
        "more2k_lessgrad_earnings", 
        "more2k_hsgrad_earnings", 
        "more2k_moregrad_earnings",
        "more2k_lessgrad_husbands",
        "more2k_hsgrad_husbands",
        "more2k_moregrad_husbands",
    ]
    
    table = table.set_index("Interactions")
    table

    model_IV_1=IV2SLS(data[outcome], data[["const", "bottom_third", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]],       data["more2k_bottomthird"], data["samesex_bottomthird"]).fit() 
    model_IV_2=IV2SLS(data[outcome], data[["const", "middle_third", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data["more2k_middlethird"], data["samesex_middlethird"]).fit()  
    model_IV_3=IV2SLS(data[outcome], data[["const", "upper_third", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data["more2k_upperthird"], data["samesex_upperthird"]).fit()  

    model_IV_4=IV2SLS(data[outcome], data[["const", "lessgrad", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data["more2k_lessgrad"], data["samesex_lessgrad"]).fit() 
    model_IV_5=IV2SLS(data[outcome], data[["const", "hsgrad", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data["more2k_hsgrad"], data["samesex_hsgrad"]).fit()  
    model_IV_6=IV2SLS(data[outcome], data[["const", "moregrad", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data["more2k_moregrad"], data["samesex_moregrad"]).fit() 
    
    model_IV_7=IV2SLS(data2[outcome], data2[["const", "lessgrad", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data2["more2k_lessgrad_earnings"], data2["samesex_lessgrad_earnings"]).fit() 
    model_IV_8=IV2SLS(data2[outcome], data2[["const", "hsgrad", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data2["more2k_hsgrad_earnings"], data2["samesex_hsgrad_earnings"]).fit()  
    model_IV_9=IV2SLS(data2[outcome], data2[["const", "moregrad", "AGEM", "agefstm", "boy1st", "blackm", "hispm", "otheracem"]], data2["more2k_moregrad_earnings"], data2["samesex_moregrad_earnings"]).fit()
    
    model_IV_10=IV2SLS(data3[outcome2], data3[["const", "AGED", "agefstd", "boy1st", "blackd", "hispd", "otheraced"]], data3["more2k"], data3["same_sex"]).fit() 
    model_IV_11=IV2SLS(data4[outcome2], data4[["const", "AGED", "agefstd", "boy1st", "blackd", "hispd", "otheraced"]], data4["more2k"], data4["same_sex"]).fit()   
    model_IV_12=IV2SLS(data5[outcome2], data5[["const", "AGED", "agefstd", "boy1st", "blackd", "hispd", "otheraced"]], data5["more2k"], data5["same_sex"]).fit()   
    
    outputs1 = [model_IV_1.params["more2k_bottomthird"],model_IV_1.std_errors["more2k_bottomthird"],]
    outputs2 = [model_IV_2.params["more2k_middlethird"],model_IV_2.std_errors["more2k_middlethird"],]
    outputs3 = [model_IV_3.params["more2k_upperthird"],model_IV_3.std_errors["more2k_upperthird"],]

    outputs4 = [model_IV_4.params["more2k_lessgrad"],model_IV_4.std_errors["more2k_lessgrad"],]
    outputs5 = [model_IV_5.params["more2k_hsgrad"],model_IV_5.std_errors["more2k_hsgrad"],]
    outputs6 = [model_IV_6.params["more2k_moregrad"],model_IV_6.std_errors["more2k_moregrad"],]

    outputs7 = [model_IV_7.params["more2k_lessgrad_earnings"],model_IV_7.std_errors["more2k_lessgrad_earnings"],]
    outputs8 = [model_IV_8.params["more2k_hsgrad_earnings"],model_IV_8.std_errors["more2k_hsgrad_earnings"],]
    outputs9 = [model_IV_9.params["more2k_moregrad_earnings"],model_IV_9.std_errors["more2k_moregrad_earnings"],]
    
    outputs10 = [model_IV_10.params["more2k"],model_IV_10.std_errors["more2k"],]
    outputs11 = [model_IV_11.params["more2k"],model_IV_11.std_errors["more2k"],]
    outputs12 = [model_IV_12.params["more2k"],model_IV_12.std_errors["more2k"],]
    
    table.loc["more2k_bottomthird"] = outputs1
    table.loc["more2k_middlethird"] = outputs2
    table.loc["more2k_upperthird"] = outputs3
    table.loc["more2k_lessgrad"] = outputs4
    table.loc["more2k_hsgrad"] = outputs5
    table.loc["more2k_moregrad"] = outputs6
    table.loc["more2k_lessgrad_earnings"] = outputs7
    table.loc["more2k_hsgrad_earnings"] = outputs8
    table.loc["more2k_moregrad_earnings"] = outputs9
    table.loc["more2k_lessgrad_husbands"] = outputs10
    table.loc["more2k_hsgrad_husbands"] = outputs11
    table.loc["more2k_moregrad_husbands"] = outputs12
    
    

    return table


def mean_samples(data, Variables_list, outcome):
    
    table = pd.DataFrame(
        {
            "Mean Dependent Variable": [],

        }
    )
    table["Variables"] = Variables_list

    table = table.set_index("Variables")

    for variable in Variables_list:

        a=data[data[variable]==1]
        mean=a[outcome].mean()
        mean=round(mean,3)

        table.loc[variable] = mean

    return table



def IV_Comparison_Models(data, outcomes, controls):

    table = pd.DataFrame(
        {
            "Same Sex (1)": [],
            "Same Sex Std.err (1)": [],
            "Twins-2 (2)": [],
            "Twins-2 Std.err (2)": [],
        }
    )
    table["outcomes"] = outcomes
    table = table.set_index("outcomes")

    for outcome in outcomes:
        
        model_IV_1=IV2SLS(data[outcome], data[controls], data["more2k"], data["same_sex"])
        result_IV_1=model_IV_1.fit()
        model_IV_2=IV2SLS(data[outcome], data[controls], data["more2k"], data[["twins"]])
        result_IV_2=model_IV_2.fit()        
        
        outputs = [
                result_IV_1.params["more2k"],
                result_IV_1.std_errors["more2k"],
                result_IV_2.params["more2k"],
                result_IV_2.std_errors["more2k"],
            
        ]
        
        table.loc[outcome] = outputs
        table = table.round(3)

    return table





def mean_differences_instruments(data, outcomes):
    
    table = pd.DataFrame(
        {
            "Mean difference by Same Sex": [],
            "Std. err.": [],
            "Mean difference by twins": [],
            "Std.err.": [],
        }
    )
    
    table["outcomes"] = outcomes
    table = table.set_index("outcomes")
    
    for outcome in outcomes:
        
        mean_samesex = data.groupby("same_sex")[outcome].mean().to_dict()
        mean_diff_samesex = mean_samesex[1] - mean_samesex[0]

        std_err_samesex = np.sqrt(
            np.power(data.loc[data["same_sex"] == 1][outcome].sem(), 2)
            + np.power(data.loc[data["same_sex"] == 0][outcome].sem(), 2)
        )
        
        mean_twins = data.groupby("twins")[outcome].mean().to_dict()
        mean_diff_twins = mean_twins[1] - mean_twins[0]

        std_err_twins = np.sqrt(
            np.power(data.loc[data["twins"] == 1][outcome].sem(), 2)
            + np.power(data.loc[data["twins"] == 0][outcome].sem(), 2)
        )
        
        outputs = [
        mean_diff_samesex,
        std_err_samesex,
        mean_diff_twins,
        std_err_twins,

        ]
        
        table.loc[outcome] = outputs
        table = table.round(4)
    
    return table




def wald_estimates_regressions(data, outcomes, instrument):

    table = pd.DataFrame(
        {
            "More than 2 children": [],
            "Std. err.": [],
            "Number of children": [],
            "Std.err.": [],
        }
    )
    table["outcomes"] = outcomes
    table = table.set_index("outcomes")

    
    for outcome in outcomes:
        
        data["more2k_predict"]=sm_api.OLS(data["more2k"], data[["const", instrument]]).fit().predict()
        wald_rslt_more2k = sm_api.OLS(data[outcome], data[["const", "more2k_predict"]]).fit() 
        
        data["children_predict"]=sm_api.OLS(data["KIDCOUNT"], data[["const", instrument]]).fit().predict()
        wald_rslt_children = sm_api.OLS(data[outcome], data[["const", "children_predict"]]).fit()  
        
        outputs = [
                wald_rslt_more2k.params["more2k_predict"],
                wald_rslt_more2k.bse["more2k_predict"],
                wald_rslt_children.params["children_predict"],
                wald_rslt_children.bse["children_predict"],


        ]
        
        table.loc[outcome] = outputs
        table = table.round(3)

    return table



