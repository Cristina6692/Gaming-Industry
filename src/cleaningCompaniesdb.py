from pymongo import MongoClient
import pandas as pd
from pandas.io.json import json_normalize
from cleaningFunc import asGeoJSON

#conectamos con la db companies
client = MongoClient("mongodb://localhost/companies")
db = client.get_database()

#seleccionamos la colección 'companies' dentro de nuestra db y convertimos a df
cursor = db["companies"].find({})
dfcompanies = json_normalize(cursor)

#nos quedamos con las columnas que nos interesan 
dfcompanies = dfcompanies[['name','category_code','total_money_raised', 'offices','founded_year']].explode('offices')

#creamos columnas al expandir la columna 'offices' y lo concatenamos todo en un mismo df ya sin la columna 'offices'
dfComp = dfcompanies[["offices"]].apply(lambda r: r.offices ,result_type="expand", axis=1)
dfcompoffi = pd.concat([dfcompanies,dfComp],axis=1)
dfcompoffi = dfcompoffi.drop(columns='offices')

#aplicamos al df la funcion 'asGeoJSON' para tener una columna location y poder utilizar geoquerys mas tarde
dfcompoffi["location"] = dfcompoffi[["latitude","longitude"]].apply(lambda x:asGeoJSON(x.latitude,x.longitude), axis=1)
dfcompclean = dfcompoffi.drop(columns=['latitude','longitude'])

#pasamos nuestro df de nuevo a formato json 
dfcompclean.to_json("cleaned_offices.json", orient="records")