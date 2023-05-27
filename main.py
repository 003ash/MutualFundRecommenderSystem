from flask import Flask, request, render_template
import pickle

file_path = "D://FYP UI//model.pkl"



app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("./index.html", title="HOME PAGE")


@app.route('/forms', methods =["POST"])
def forms():
    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    age = request.form.get("age")
    income = request.form.get("income")
    expense = request.form.get("expense")
    dependants = request.form.get("depandants")
    # fund_type = request.form.get("fund_type")
    # risk = request.form.get("risk")
    investment_amt = request.form.get("investment_amt")
    duration = request.form.get("duration")
    investment_type = request.form.get("investment_type")
    
    #Now transform the data as needed
    #name=first_name+last_name
    
    #Add all the data to array inputs
    inputs=[]
    #inputs.append(name)
    
    with open(file_path, "rb") as file:
        model = pickle.load(file)
        output=model.predict(inputs)
    
    return render_template("./output.html",output=output ,title="HOME PAGE")
    


if __name__ == "__main__":
    app.run(debug=True)



