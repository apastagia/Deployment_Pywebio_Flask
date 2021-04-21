from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

import pickle
import numpy as np

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
app = Flask(__name__)

def predict():
    Year = input("Enter model Year: ", type=NUMBER)
    Year = 2021 - Year
    Present_Price = input("Enter Present Price(in LAKHS): ", type=FLOAT)
    Kms_Driven = input("Enter distance it has travelled(in KMS): ", type=FLOAT)
    Kms_Driven2 = np.log(Kms_Driven)
    Owner = input("Enter number of owners who have previously owned it(0 or 1 or 2 or 3): ", type = NUMBER)
    
    Fuel_type = select('What is the fuel type', ['Petrol','Diesel','CNG'])
    if (Fuel_type == 'Petrol'):
        Fuel_type = 239

    elif(Fuel_type == 'Diesel'):
        Fuel_type = 60

    else:
        Fuel_type = 2

    Seller_Type = select('Dealer or Individual?', ['Dealer', 'Individual'])
    if Seller_Type == 'Individual':
        Seller_Type = 106
    else:
        Seller_Type = 195

    Transmission = select('Transmission Type', ['Manual Car', 'Automatic Car'])
    if Transmission == 'Manual Car':
        Transmission = 261
    else:
        Transmission = 40

    prediction = model.predict([[Present_Price, Kms_Driven2,Fuel_type,Seller_Type,Transmission,Owner,Year]])
    output = round(prediction[0],2)

    if output < 0:
        put_text('Sorry you can not sell this car')

    else:
        put_text('Sell this car at ', output, 'price')

app.add_url_rule('/tool','webio_view', webio_view(predict),
                    methods = ['GET','POST','OPTIONS'])
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)
'''
app.run(host='localhost', port=80)