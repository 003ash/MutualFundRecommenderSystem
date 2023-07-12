from flask import Flask, request, render_template
import pickle
from bs4 import BeautifulSoup
from functions import recommended_funds, duration_dic, final_score

import pandas as pd
import numpy as np
   
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

   #get features from the form
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

   #calculate score
   (fundTypeList, riskCapacity) = final_score(agePt+empStatusPt+incomePt+investmentObjectivePt+riskTolerancePt+investmentDuration)  

   #get output  
   output=recommended_funds(fundTypeList,riskCapacity,minInvestment,duration_dic[investmentDuration])

   #format output
   output = output.drop(['Fund_Manager_Tenure','Return_3m','Return_3yr'], axis=1)
   output = output.reset_index(drop=True)
   output.index = np.arange(1, len(output) + 1)
   output["Category"] = output["Category"].apply(getName)
   output.rename(columns = {'Return_1wk':'1 Week Returns','Return_1m':'1 Month Returns','Return_6m':'6 Month Returns','Return_1yr':'1 Year Returns','Return_5yr':'5 Year Returns','Return_10yr':'10 Year Returns'}, inplace = True)
   output=output.to_html().replace('<td>', '<td align="center">').replace('<th>', '<th align="center">')

   return render_template("output.html",output=output, name=first_name+" "+last_name ,title="HOME PAGE")
    

if __name__ == "__main__":
    app.run(debug=True)



