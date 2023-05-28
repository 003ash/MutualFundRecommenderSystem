from flask import Flask, request, render_template
import pickle

import pandas as pd
import numpy as np

file_path = "recommender\ProcessedData2_with_cluster.csv"
df_w_cluster = pd.read_csv(file_path)

risk_dic = {"Conservative":1,"Moderately Conservative":2,"Moderately Agressive":3,
            "Aggressive":4,"Very Agressive":5}
fund_type_dic = {'Equity':'Category_Equity',
                 'Debt':'Category_Debt',
                 'Hybrid':'Category_Hybrid'}
duration_dic = {0.25: 'Return_1wk',1: 'Return_1m', 3:'Return_3m', 
                6:'Return_6m', 12: 'Return_1yr', 36:'Return_3yr', 
                60:'Return_5yr', 120:'Return_10yr'}

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

def recommended_funds(Fund_type,Risk_profile,Min_inves,Duration_of_investment):
    # filter_features = ['#_Funds_managed']
     
    # dur = duration_dic[translate_duration(Duration_of_investment)]
    dur = Duration_of_investment
    risk_quantile = risk_dic[Risk_profile]/len(risk_dic)     # Risk quantile [0.2, 0.4, 0.6 , 0.8, 1]
    # red_delay_min = Red_Delay[0]
    # red_delay_max = Red_Delay[1]
    min_inv= Min_inves
#     comp_quant_min = comp_size_dic[cpy_size][0]
#     comp_quant_max = comp_size_dic[cpy_size][1]
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
    result = new_df[new_df['kmeans_1']==final_cluster][['Scheme_name','Category','Fund_Manager_Tenure','Return_1m','Return_3m','Return_6m']].sort_values(by=['Fund_Manager_Tenure',dur],ascending = False).head()
    return result 

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
   


app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html", title="HOME PAGE")


@app.route('/forms', methods =["POST"])
def forms():
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

    fundType = determineFundType(reactionTo10DeclinePt+highRiskAllocationPt)
    riskCapacity = detrmineRiskCapacity(agePt+empStatusPt+incomePt+investmentObjectivePt+riskTolerancePt)
    
    #Now transform the data as needed
    #name=first_name+last_name
    
    #Add all the data to array inputs
    # inputs=[]
    #inputs.append(name)
    
    with open(file_path, "rb") as file:
        output=recommended_funds(fundType,riskCapacity,minInvestment,duration_dic[investmentDuration])
    
    return render_template("output.html",output=output ,title="HOME PAGE")
    


if __name__ == "__main__":
    app.run(debug=True)



