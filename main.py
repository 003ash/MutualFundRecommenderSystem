from flask import Flask, request, render_template
import pickle
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

file_path = "ProcessedData2_with_cluster.csv"
df_w_cluster = pd.read_csv(file_path)

risk_dic = {"Conservative":1,"Moderately Conservative":2,"Moderately Aggressive":3,
            "Aggressive":4,"Very Aggressive":5}
fund_type_dic = {'Equity':'Category_Equity',
                 'Debt':'Category_Debt',
                 'Hybrid':'Category_Hybrid'}
duration_dic = {8: 'Return_1wk',7: 'Return_1m', 6:'Return_3m', 
                5:'Return_6m', 4: 'Return_1yr', 3:'Return_3yr', 
                2:'Return_5yr', 1:'Return_10yr'}

list_keys = duration_dic.keys()
def round_ceiling(number):
  if number>=120:
    return 120
  else:
    return min(i for i in list_keys if i >= number)
  
#input in the form of number of months (n_m) where n is the number
# def translate_duration(dur):
#     n = float(dur.split('_')[0])
#     return round_ceiling(n)

def recommended_funds(fund_type_list,Risk_profile,Min_inves,Duration_of_investment):
    # filter_features = ['#_Funds_managed']
   
    # dur = duration_dic[translate_duration(Duration_of_investment)]
    dur = Duration_of_investment
    risk_quantile = risk_dic[Risk_profile]/len(risk_dic)     # Risk quantile [0.2, 0.4, 0.6 , 0.8, 1]
    # red_delay_min = Red_Delay[0]
    # red_delay_max = Red_Delay[1]
    min_inv= Min_inves
    df_list = []
    for Fund_type in fund_type_list:
      if Fund_type=='Equity':
         new_df = df_w_cluster.loc[ #(df_w_cluster['Liquidity Ratios'] >= red_delay_min) &
                  #(df_w_cluster['Liquidity Ratios'] <= red_delay_max) &
                  (df_w_cluster['Minimum_Investment'] <= min_inv) & 
                  (df_w_cluster['Category_Equity'] == 1) &
                  (df_w_cluster['Category_Debt'] == 0) &
                  (df_w_cluster['Category_Hybrid'] == 0) 
                  ]  
      elif Fund_type=='Debt':
         new_df = df_w_cluster.loc[ #(df_w_cluster['Liquidity Ratios'] >= red_delay_min) &
                  #(df_w_cluster['Liquidity Ratios'] <= red_delay_max) &
                  (df_w_cluster['Minimum_Investment'] <= min_inv) & 
                  (df_w_cluster['Category_Equity'] == 0) &
                  (df_w_cluster['Category_Debt'] == 1) &
                  (df_w_cluster['Category_Hybrid'] == 0) 
                  ]
      elif Fund_type=='Hybrid':
         new_df = df_w_cluster.loc[ #(df_w_cluster['Liquidity Ratios'] >= red_delay_min) &
                  #(df_w_cluster['Liquidity Ratios'] <= red_delay_max) &
                  (df_w_cluster['Minimum_Investment'] <= min_inv) & 
                  (df_w_cluster['Category_Equity'] == 0) &
                  (df_w_cluster['Category_Debt'] == 0) &
                  (df_w_cluster['Category_Hybrid'] == 1) 
                  ] 

      vol_quantile_value = new_df['Standard Deviation'].quantile(risk_quantile)
      vol_clust_mean = new_df.groupby(['kmeans_1'])['Standard Deviation'].agg([np.mean]).sort_values(by=['mean'],ascending = False)
      vol_clust_mean['dif'] = vol_clust_mean['mean'].map(lambda x: np.absolute(x-vol_quantile_value))
      final_cluster = vol_clust_mean.sort_values(by=['dif']).index[0]
      print("Final Cluster: " + str(final_cluster))
      print('There are {} results '.format(new_df.shape[0]))
      print("Top 5 returns: ")
      result = new_df[new_df['kmeans_1']==final_cluster][['Scheme_name','Category','Fund_Manager_Tenure','Return_1wk','Return_1m','Return_3m','Return_6m','Return_1yr','Return_3yr','Return_5yr','Return_10yr']]
      df_list.append(result)
    r1 = pd.concat(df_list)
    r1 = r1.sort_values(by=[dur,'Fund_Manager_Tenure'],ascending = False).head()
    return r1
#     comp_quant_min = comp_size_dic[cpy_size][0]
#     comp_quant_max = comp_size_dic[cpy_size][1]
   #  if Fund_type=='Equity':
   #    new_df = df_w_cluster.loc[ #(df_w_cluster['Liquidity Ratios'] >= red_delay_min) &
   #               #(df_w_cluster['Liquidity Ratios'] <= red_delay_max) &
   #               (df_w_cluster['Minimum_Investment'] <= min_inv) & 
   #               (df_w_cluster['Category_Equity'] == 1) &
   #               (df_w_cluster['Category_Debt'] == 0) &
   #               (df_w_cluster['Category_Hybrid'] == 0) 
   #              ]  
   #  elif Fund_type=='Debt':
   #    new_df = df_w_cluster.loc[ #(df_w_cluster['Liquidity Ratios'] >= red_delay_min) &
   #               #(df_w_cluster['Liquidity Ratios'] <= red_delay_max) &
   #               (df_w_cluster['Minimum_Investment'] <= min_inv) & 
   #               (df_w_cluster['Category_Equity'] == 0) &
   #               (df_w_cluster['Category_Debt'] == 1) &
   #               (df_w_cluster['Category_Hybrid'] == 0) 
   #              ]
   #  elif Fund_type=='Hybrid':
   #    new_df = df_w_cluster.loc[ #(df_w_cluster['Liquidity Ratios'] >= red_delay_min) &
   #               #(df_w_cluster['Liquidity Ratios'] <= red_delay_max) &
   #               (df_w_cluster['Minimum_Investment'] <= min_inv) & 
   #               (df_w_cluster['Category_Equity'] == 0) &
   #               (df_w_cluster['Category_Debt'] == 0) &
   #               (df_w_cluster['Category_Hybrid'] == 1) 
   #              ] 

   #  vol_quantile_value = new_df['Standard Deviation'].quantile(risk_quantile)
   #  vol_clust_mean = new_df.groupby(['kmeans_1'])['Standard Deviation'].agg([np.mean]).sort_values(by=['mean'],ascending = False)
   #  vol_clust_mean['dif'] = vol_clust_mean['mean'].map(lambda x: np.absolute(x-vol_quantile_value))
   #  final_cluster = vol_clust_mean.sort_values(by=['dif']).index[0]
   #  print("Final Cluster: " + str(final_cluster))
   #  print('There are {} results '.format(new_df.shape[0]))
   #  print("Top 5 returns: ")
   #  result = new_df[new_df['kmeans_1']==final_cluster][['Scheme_name','Category','Fund_Manager_Tenure','Return_1wk','Return_1m','Return_3m','Return_6m','Return_1yr','Return_3yr','Return_5yr','Return_10yr']].sort_values(by=['Fund_Manager_Tenure',dur],ascending = False).head()
   #  return result 

def detrmineRiskCapacity(pts):
   if pts>=21:
      return "Very Aggressive"
   elif pts>=18:
      return "Aggressive"
   elif pts>=15:
      return "Moderately Aggressive"
   elif pts>=12:
      return "Moderately Conservative"
   else:
      return "Conservative"
   
def determineFundType(pts):
   if pts>=7:
      return "Equity"
   elif pts>=5:
      return "Hybrid"
   else:
      return "Debt"

def final_score(pts):
   if pts<10:
      return (["Debt"],"Conservative")
   elif pts<=14:
      return (["Debt", "Hybrid"],"Moderately Conservative")
   elif pts<=19:
      return (["Hybrid"], "Moderately Aggressive")
   elif pts<=24:
      return (["Hybrid","Equity"], "Aggressive")
   else:    
      return (["Equity"], "Very Aggressive")  
   



app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html", title="HOME PAGE")


@app.route('/forms', methods =["POST"])
def forms():
    def getName(name):
      if name[0] == 'H':
         return 'Hybrid'
      elif name[0] == 'D':
         return 'Debt'
      elif name[0] == 'E':
         return 'Equity'


    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    agePt = int(request.form.get("age"))
    empStatusPt = int(request.form.get("empStatus"))
    incomePt = int(request.form.get("income"))
    minInvestment = int(request.form.get("minInvestment"))
    investmentObjectivePt = int(request.form.get("investmentObjective"))
    investmentDuration = float(request.form.get("investmentDuration"))
    riskTolerancePt = int(request.form.get("riskTolerance"))
    reactionTo10DeclinePt = int(request.form.get("reactionTo10%Decline"))
    highRiskAllocationPt = int(request.form.get("highRiskAllocation"))

   #  fundType = determineFundType(reactionTo10DeclinePt+highRiskAllocationPt)
   #  riskCapacity = detrmineRiskCapacity(agePt+empStatusPt+incomePt+investmentObjectivePt+riskTolerancePt)
    (fundTypeList, riskCapacity) = final_score(agePt+empStatusPt+incomePt+investmentObjectivePt+riskTolerancePt+investmentDuration)
    print(type(fundTypeList), type(riskCapacity))
    #Now transform the data as needed
    #name=first_name+last_name
    
    #Add all the data to array inputs
    # inputs=[]
    #inputs.append(name)
    
    with open(file_path, "rb") as file:
        output=recommended_funds(fundTypeList,riskCapacity,minInvestment,duration_dic[investmentDuration])
        print(output.head())
        output = output.drop(['Fund_Manager_Tenure','Return_3m','Return_3yr'], axis=1)
        output = output.reset_index(drop=True)
        output.index = np.arange(1, len(output) + 1)
        output["Category"] = output["Category"].apply(getName)
        output.rename(columns = {'Return_1wk':'1 Week Returns','Return_1m':'1 Month Returns','Return_6m':'6 Month Returns','Return_1yr':'1 Year Returns','Return_5yr':'5 Year Returns','Return_10yr':'10 Year Returns'}, inplace = True)
        output=output.to_html().replace('<td>', '<td align="center">').replace('<th>', '<th align="center">')
    return render_template("output.html",output=output, name=first_name+" "+last_name ,title="HOME PAGE")
    

if __name__ == "__main__":
    app.run(debug=True)



