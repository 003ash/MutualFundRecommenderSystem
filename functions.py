import pandas as pd
import numpy as np

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

def recommended_funds(fund_type_list,Risk_profile,Min_inves,Duration_of_investment):
    file_path = "ProcessedData2_with_cluster.csv"
    df_w_cluster = pd.read_csv(file_path)
    dur = Duration_of_investment
    risk_quantile = risk_dic[Risk_profile]/len(risk_dic)     # Risk quantile [0.2, 0.4, 0.6 , 0.8, 1]
    min_inv= Min_inves
    df_list = []
    for Fund_type in fund_type_list:
        if Fund_type=='Equity':
            new_df = df_w_cluster.loc[
                    (df_w_cluster['Minimum_Investment'] <= min_inv) & 
                    (df_w_cluster['Category_Equity'] == 1) &
                    (df_w_cluster['Category_Debt'] == 0) &
                    (df_w_cluster['Category_Hybrid'] == 0) 
                    ]  
        elif Fund_type=='Debt':
            new_df = df_w_cluster.loc[ 
                    (df_w_cluster['Minimum_Investment'] <= min_inv) & 
                    (df_w_cluster['Category_Equity'] == 0) &
                    (df_w_cluster['Category_Debt'] == 1) &
                    (df_w_cluster['Category_Hybrid'] == 0) 
                    ]
        elif Fund_type=='Hybrid':
            new_df = df_w_cluster.loc[ 
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