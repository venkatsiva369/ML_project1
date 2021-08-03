from flask import Flask, redirect, url_for, render_template, request
import pickle
import numpy as np
import jsonify
import requests
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/', methods = ['GET'])
def welcome():
    return render_template('index.html')

standard_to = StandardScaler()

@app.route('/predict', methods = ['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['year'])
        no_year = 2021 - Year
        Present_Price = float(request.form['current_price'])
        Kms_Driven = int(request.form['km_driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['owner'])
        Fuel_Type_Petrol = request.form['fuel_type_petrol']
        if (Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        Seller_Type_Individual = request.form['Seller_type_individual']
        if (Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Manual = request.form['transmission_mannual']
        if (Transmission_Manual == 'Mannual'):
            Transmission_Manual = 1
        else:
            Transmission_Manual =0
        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, no_year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual ]])
        output = round(prediction[0],2)
        if output < 0:
            return render_template('index.html', prediction_text ="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text = "You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
