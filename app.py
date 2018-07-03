###########################
# Dependencies
###########################
#Set up Flask (Server)
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for)

#SQL Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, select
from flask_sqlalchemy import SQLAlchemy


import pandas as pd, json
import numpy as np
import os

###########################
# Convert Json to GeoJson
###########################
def df_to_geojson(df, properties, lat='Y', lon='X'):

# create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                'properties':{},
                'geometry':{'type':'Point',
                            'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson


###########################
# Flask Setup
###########################
#create the engine with sqlite
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db/crimedata2017.sqlite"

engine = create_engine("sqlite:///db/crimedata.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Crime2017 = Base.classes.crimedata2017
Crime2018 = Base.classes.crimedata2018

#################################################
# Database Setup
#################################################

#db = SQLAlchemy(app)
session = Session(engine)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/mapbox/dark")
def sfmapboxdark():
    json_data = os.path.join(app.static_folder, 'style.json')
    with open(json_data) as blog_file:
        data = json.load(blog_file)
        return jsonify(data)

@app.route("/api/crimedata/sfgrid")
def sfgrid():
    json_data = os.path.join(app.static_folder, 'sfneighborhoods.geojson')
    with open(json_data) as blog_file:
        data = json.load(blog_file)
        return jsonify(data)


@app.route("/api/crimedata/2018/theft")
def crimedata2018theft():
   
    #Grab all the columns we need and create a list
    sel2018 = [Crime2018.IncidntNum,
        Crime2018.Category,
        Crime2018.Descript,
        Crime2018.DayOfWeek,
        Crime2018.Date,
        Crime2018.Time,
        Crime2018.PdDistrict,
        Crime2018.Resolution,
        Crime2018.Address,
        Crime2018.X,
        Crime2018.Y]    

    results2018 = session.query(*sel2018).\
        filter(Crime2018.Category == "LARCENY/THEFT").all()
        
    #Store results into a dataframe
    df = pd.DataFrame(results2018, columns=['IncidntNum','Category','Descript',
                                        'DayOfWeek', 'Date', 'Time', 'PdDistrict',
                                        'Resolution', 'Address', 'X', 'Y'])


    # useful_columns  = ['IncidntNum','Category','Descript',
    #                                 'DayOfWeek', 'Date', 'Time', 'PdDistrict',
    #                                 'Resolution', 'Address', 'X', 'Y']

    # geojson_dict = df_to_geojson(df, properties=useful_columns)

    #Return the dataframe in json format
    return jsonify(df.to_dict(orient="records"))    
    

##Assault End Point    
@app.route("/api/crimedata/2018/assault")
def crimedata2018assault():
   
    #Grab all the columns we need and create a list
    sel2018 = [Crime2018.IncidntNum,
        Crime2018.Category,
        Crime2018.Descript,
        Crime2018.DayOfWeek,
        Crime2018.Date,
        Crime2018.Time,
        Crime2018.PdDistrict,
        Crime2018.Resolution,
        Crime2018.Address,
        Crime2018.X,
        Crime2018.Y]    

    results2018 = session.query(*sel2018).\
        filter(Crime2018.Category == "ASSAULT").all()
        
    #Store results into a dataframe
    df = pd.DataFrame(results2018, columns=['IncidntNum','Category','Descript',
                                        'DayOfWeek', 'Date', 'Time', 'PdDistrict',
                                        'Resolution', 'Address', 'X', 'Y'])


    # useful_columns  = ['IncidntNum','Category','Descript',
    #                                 'DayOfWeek', 'Date', 'Time', 'PdDistrict',
    #                                 'Resolution', 'Address', 'X', 'Y']

    # geojson_dict = df_to_geojson(df, properties=useful_columns)

    #Return the dataframe in json format
    return jsonify(df.to_dict(orient="records"))    

 #Assault End Point    
@app.route("/api/crimedata/2018/vandalism")
def crimedata2018vandalism():
   
    #Grab all the columns we need and create a list
    sel2018 = [Crime2018.IncidntNum,
        Crime2018.Category,
        Crime2018.Descript,
        Crime2018.DayOfWeek,
        Crime2018.Date,
        Crime2018.Time,
        Crime2018.PdDistrict,
        Crime2018.Resolution,
        Crime2018.Address,
        Crime2018.X,
        Crime2018.Y]    

    results2018 = session.query(*sel2018).\
        filter(Crime2018.Category == "VANDALISM").all()
        
    #Store results into a dataframe
    df = pd.DataFrame(results2018, columns=['IncidntNum','Category','Descript',
                                        'DayOfWeek', 'Date', 'Time', 'PdDistrict',
                                        'Resolution', 'Address', 'X', 'Y'])


    # useful_columns  = ['IncidntNum','Category','Descript',
    #                                 'DayOfWeek', 'Date', 'Time', 'PdDistrict',
    #                                 'Resolution', 'Address', 'X', 'Y']

    # geojson_dict = df_to_geojson(df, properties=useful_columns)

    #Return the dataframe in json format
    return jsonify(df.to_dict(orient="records"))    

if __name__ == "__main__":
    app.run(debug=True)

#1. Read in CSV into python
#2. Create a sqllite database out of it
#3. Import this database into python and create an engine with automap
#4. Configure the endpoint to return a json