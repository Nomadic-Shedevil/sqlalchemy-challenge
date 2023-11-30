# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return ('''
        <h1>Welcome to the Climate Analysis API!</h1>
        <h2>Available Routes:</h2>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/temp/start<br/>
        /api/v1.0/temp/start/end
        ''')
   


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    precipitation = list(np.ravel(results))
    return jsonify(precipitation=precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.station).all()
    session.close()
    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations"""
    # Query all temperature observations
    results = session.query(Measurement.tobs).all()
    session.close()
    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))
    return jsonify(tobs=tobs)

@app.route('/api/v1.0/temp/start')
def stats(start=None, end=None):
    # Query all temperature observations   
    #define my functions for min, max, avg
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
    #define my start and end dates and format
        #start = dt.datetime.strptime(start, '%Y%m%d')
        results = session.query(*sel).filter(Measurement.date != start).all()
        session.close()
    # Convert list of tuples into normal list
        temps = list(np.ravel(results))
        return jsonify(temps=temps)


@app.route('/api/v1.0/temp/start/end')
def statistics(start=None, end=None):
    
    #define my functions for min, max, avg
    stats = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
    #define my start and end dates and format
        #start = dt.datetime.strptime(start, '%Y%m%d')
        #end = dt.datetime.strptime(end, '%Y%m%d')
    
    #put in my session query based on my date formats specified above
        results = session.query(*stats).filter(Measurement.date != start).filter(Measurement.date != end).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
#     # if end != None: 
#     #     # Query all temperature observations
#     #     results = session.query(Measurement.tobs).filter(Measurement.date >= start,Measurement.date <= end).all()
#     #     session.close()
#     #     # Convert list of tuples into normal list
#     #     temps = list(np.ravel(results))
#     #     return jsonify(temps=temps)
#     # elif end == None:
#     #     # Query all temperature observations
#     #     results = session.query(Measurement.tobs).filter(Measurement.date >= start).all()
#     #     session.close()
#     #     # Convert list of tuples into normal list
#     #     temps = list(np.ravel(results))
#     #     return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)
    