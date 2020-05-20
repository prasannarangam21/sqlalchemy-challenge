import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# Create an app, being sure to pass __name__
app = Flask(__name__)
prev_date = dt.date(2017,8,23) - dt.timedelta(days=365)
# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (
        
        f"<h1>Hawaii Precipitation and Weather Data<br/></h1>"
        f"<h2>Pick from the below available routes:<br/></h2>"
      #  f"<b>For Precipitation<br/></b>"
        f"<a href="http://127.0.0.1:5000/api/v1.0/precipitation">/api/v1.0/precipitation</a>"
        f"<b>For the list of all weather stations in Hawaii<br/></b>"
        f"/api/v1.0/stations<br/>"
        f"<b>For the Temperature Observations (tobs)<br/></b>"
        f"/api/v1.0/tobs<br/>"
        f"<b>For checking the Start Statistics for Start range<br/></b>"
        f"/api/v1.0/temp/start<br/>"
        f"<b>For checking the Start-end Statistics for Start-End range<br/></b>"
        f"/api/v1.0/temp/start/end"
        
        
        )  
# Define what to do when a user hits the /precicpitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
# Query the date and precipitation values 
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > prev_date).order_by(measurement.date).all()
# getting the date and prcp data from results into precipitation data dictionary 
    precipitation_data = {date:prcp for date,prcp in results}
"""Return the precipitation data as json"""
    return jsonify(precipitation_data)
# Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")
def stations():
"""Return a list of all station names"""
# Query all stations
    results = session.query(station.station).all()
# Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
"""Return the stations data as json"""
    return jsonify(all_stations)
# Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= prev_date).all()
# Convert list of tuples into normal list
    temp_data = list(np.ravel(results))
"""Return the temperature data as json"""
    return jsonify(temp_data)
# Define what to do when a user hits the /<start> route
@app.route("/api/v1.0/temp/<start>")
# Define what to do when a user hits the /<start>/<end> route
@app.route("/api/v1.0/temp/<start>/<end>")
def startend(start=None,end=None):
"""Return a json list of the min temperature, the max temperature, and the avg temperature for a given start date"""
# if end is null 
    if not end:
        results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).all()
"""Return the start end data as json"""
# Convert list of tuples into normal list
        start_only = list(np.ravel(results))
        return jsonify(start_only)    
"""Return a json list of the min temperature, the max temperature, and the avg temperature for a given start-end date range."""        
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
# Convert list of tuples into normal list
    start_end = list(np.ravel(results))
    return jsonify(start_end)
if __name__ == "__main__":
    app.run(debug=True)