
from flask import Flask, jsonify
from sqlalchemy.sql import text
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station



# Flask setup

app = Flask(__name__)

# Homepage and List of Available Flask Routes


@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii Precipitation Information Page API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


# Precipitation Route:

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    previous_twelve_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    past_12_months_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_twelve_months).all()

# Close Session
    
    session.close()
    
# Convert the query results from the precipitation analysis to a dictionary using date as the key and prcp as the value.

    precip = {date: prcp for date, prcp in past_12_months_prcp}
    return jsonify(precip)


# Stations Route:

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

# Query the data for list of Stations

    stations_listing = session.query(Measurement.station).distinct().all()


    session.close()

# Return a JSON list of stations from the dataset.

    station = [station[0] for station in stations_listing]
    return jsonify(stations=station)


# Temperature Route:

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)

# Query the dates and temperature observations of the most-active station for the previous year of data.

    previous_twelve_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    past_12_months_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= previous_twelve_months).all()

    session.close()

# Return a JSON list of temperature observations for the previous year.

    temp = [tobs for date, tobs in past_12_months_temp]
    return jsonify(temps=temp)

# Start and Start-End Routes

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start_end(start=None, end=None):
    session = Session(engine)
    """Return TMIN, TAVG, TMAX."""

# Calculate the minimum, average, and maximum temperatures for all the dates greater than or equal to the start date.

    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]

    # convert parameter "start_end" into proper datetime format
    # start = dt.datetime.strptime(start, "%Y-%m-%d")
    # end = dt.datetime.strptime(end, "%Y-%m-%d")


    if not end:

    # <Start> Route

        data = session.query(*sel).\
        filter(Measurement.date >= start).all()

        session.close()

# convert data into list format
        temp_results = list(np.ravel(data))

# Convert list into json format
        return jsonify(temp_results)

# <Start-End> Route

    data = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    session.close()

# convert data into list format
    temp_results = list(np.ravel(data))

# Convert list into json format
    return jsonify(temp_results)



if __name__ == '__main__':
    app.run(debug=True)


