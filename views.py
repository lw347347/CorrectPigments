from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import VehicleSale
from api.serializers import CampaignSearchSerializer
# from api.models import Donation
# from api.serializers import DonationSerializer
# from api.models import Update
# from api.serializers import UpdateSerializer

import json
import stripe
import math

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

import pyodbc 

class VehicleSalesInput(APIView):
    @csrf_exempt
    def get(self, request, format=None):
    # this view receives parameters from the submit html template and calls the API in azure
    # this contains API code for Python and Python3

        # Grab the inputs from formik
        manufacturer = request.query_params.get('manufacturer')
        condition = request.query_params.get('condition')
        cylinders = request.query_params.get('cylinders')
        fuel = request.query_params.get('fuel')
        odometer = request.query_params.get('odometer')
        title_status = request.query_params.get('title_status')
        transmission = request.query_params.get('transmission')
        drive = request.query_params.get('drive')
        vehicle_type = request.query_params.get('vehicle_type')
        paint_color = request.query_params.get('paint_color')
        model = request.query_params.get('model')
        state = request.query_params.get('state')
        description = request.query_params.get('description')
        description_language = request.query_params.get('description_language')
        price = request.query_params.get('price')
        year = request.query_params.get('year')

        # # Establish a connection to my database server
        # try:
        #     connection = mysql.connector.connect(host='vehiclesdatabase.cdagoin9cxtz.us-east-1.rds.amazonaws.com',
        #                                         database='innodb',
        #                                         user='admin',
        #                                         password='347LD415')
        #     cursor = connection.cursor(prepared=True)

        #     mySql_insert_query = """INSERT INTO vehicles (price, year, manufacturer, model, `condition`, cylinders, 
        #                                 fuel, odometer, title_status, transmission, drive, `type`, paint_color, 
        #                                 description, state, description_language) 
        #                         VALUES 
        #                         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        #     insert_tuple_1 = (price, year, manufacturer, model, condition, cylinders, fuel, odometer, title_status,
        #                     transmission, drive, vehicle_type, paint_color, description, state, description_language)

        #     cursor.execute(mySql_insert_query, insert_tuple_1)
        #     connection.commit()
        #     cursor.close()
        # Connect to the database in Azure
        # Establish a connection to my database server
        connection = pyodbc.connect('Driver={SQL Server};'
                                            'Server=is415.database.windows.net;'
                                            'Database=is415Database;'
                                            'UID=serverAdmin;'
                                            'PWD=347!d415;')
        cursor = connection.cursor()

        # Create the SQL
        SQLServer_insert_query = """INSERT INTO vehicleSales (price, year, manufacturer, model, condition, cylinders, 
                                            fuel, odometer, title_status, transmission, drive, type, paint_color, 
                                            description, state, description_language) 
                                    VALUES 
                                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        # Input the parameterized parameters
        insert_tuple_1 = (price, year, manufacturer, model, condition, cylinders, fuel, odometer, title_status,
                                transmission, drive, vehicle_type, paint_color, description, state, description_language)

        # Insert into the database
        cursor.execute(SQLServer_insert_query, insert_tuple_1)
        connection.commit()
        cursor.close()
               
       
        return Response('Success')

class PredictionCalculator(APIView):
    @csrf_exempt
    def get(self, request, format=None):
    # this view receives parameters from the submit html template and calls the API in azure
    # this contains API code for Python and Python3 

        # If you are using Python 3+, import urllib instead of urllib2
        #import urllib2.request
        import urllib
        import json 

        # Grab the inputs from formik
        manufacturer = request.query_params.get('manufacturer')
        condition = request.query_params.get('condition')
        cylinders = request.query_params.get('cylinders')
        fuel = request.query_params.get('fuel')
        odometer = request.query_params.get('odometer')
        title_status = request.query_params.get('title_status')
        transmission = request.query_params.get('transmission')
        drive = request.query_params.get('drive')
        vehicle_type = request.query_params.get('vehicle_type')
        paint_color = request.query_params.get('paint_color')
        model = request.query_params.get('model')
        state = request.query_params.get('state')
        description = request.query_params.get('description')
        description_language = request.query_params.get('description_language')
        price = request.query_params.get('price')
        year = request.query_params.get('year')
        
        # formatting the data into a data object for the API call
        data =  {
                "Inputs": {
                    "input1": {
                    "ColumnNames": [
                        "year",
                        "manufacturer",
                        "condition",
                        "cylinders",
                        "fuel",
                        "odometer",
                        "transmission",
                        "drive",
                        "type",
                        "description",
                        "state",
                        "description_language"
                    ],
                    "Values": [
                        [
                        year,
                        manufacturer,
                        condition,
                        cylinders,
                        fuel,
                        odometer,
                        transmission,
                        drive,
                        vehicle_type,
                        description,
                        state,
                        description_language
                        ]
                    ]
                    }
                },
                "GlobalParameters": {}
                }

        # the API call
        body = str.encode(json.dumps(data))
        url = 'https://ussouthcentral.services.azureml.net/workspaces/b7fcea30955b4e65baaa8dfa89044435/services/35cad3add1004d59a158b7e68f8bbb81/execute?api-version=2.0&details=true'
        api_key = 'pFiDEHgMTLArS5/3Rhe5dEMIjWnM4bYmHUYudj5bc6klDcxm8VPzc4/UKuRoduTCil+HAqEOFqsuAk3Vd5Mfxg=='
        # Replace my url and api_key with your own values
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        # If you are using Python 3+, replace urllib2 with urllib.request
        #req = urllib2.Request(url, body, headers)
        req = urllib.request.Request(url, body, headers) 

        # python3 uses urllib while python uses urllib2
        #response = urllib2.request.urlopen(req)
        response = urllib.request.urlopen(req)

        # this formats the results 
        result = response.read()
        result = json.loads(result) # turns bits into json object
        totalPrice = result["Results"]["output1"]["value"]["Values"][0][0]

        totalPrice = round(float(totalPrice)**2, 2)

        responseForReact = [totalPrice]
        
        # serializer = PredictionCalculatorSerializer(cats, many=True)
        return Response(responseForReact)