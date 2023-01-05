
from flask import Flask, jsonify
from sqlalchemy.sql import text
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


# Flask setup

app = Flask(__name__)

# Flask Routes


@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii Precipitation Information Page API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_twelve_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    past_12_months_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_twelve_months).all()
    
    session.close()
    
     
    precip = {date: prcp for date, prcp in past_12_months_prcp}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def station():
    stations_listing = session.query(Measurement.station).distinct().all()

    session.close()

    # station = {date: station for date, station in stations_listing}
    station = [station[0] for station in stations_listing]
    return jsonify(stations=station)


@app.route("/api/v1.0/tobs")
def temperature():
    previous_twelve_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    past_12_months_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= previous_twelve_months).all()

    session.close()


    temp = [tobs for date, tobs in past_12_months_temp]
    return jsonify(temps=temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:

# convert parameter "start" into proper datetime format

        start= dt.datetime.strptime(start, "%m-%d-%Y")
        data = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

# convert data into list format
        starting_temp = list(np.ravel(data))

# Convert list into json format
        return jsonify(starting_temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start_end(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]


        # convert parameter "start_end" into proper datetime format

    start = dt.datetime.strptime(start, "%m-%d-%Y")
    end = dt.datetime.strptime(end, "%m-%d-%Y")
    start_end_data = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    session.close()

# convert data into list format
    start_end_temp = list(np.ravel(start_end_data))

# Convert list into json format
    return jsonify(start_end_temp)


# @app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")
# def start(start=None, end=None):
#     """Return TMIN, TAVG, TMAX."""

#     sel = [func.min(Measurement.tobs), func.avg(
#         Measurement.tobs), func.max(Measurement.tobs)]

#     if not end:

#         # convert parameter "start" into proper datetime format

#         start = dt.datetime.strptime(start, "%m-%d-%Y")
#         end = dt.datetime.strptime(end, "%m-%d-%Y")
#         data =  session.query(*sel).\
#             filter(Measurement.date >= start).\
#             filter(Measurement.date <= end).all()
#         start= session.query(*sel).\
#         filter(Measurement.date >= start).\
#         filter(Measurement.date <= end).all()

#         session.close()

# # convert data into list format
#         start_end_temp = list(np.ravel(data))
#         start_end_temp = list(np.ravel(start_end_data))

# # Convert list into json format
#         return jsonify(start_end_temp)
        


if __name__ == '__main__':
    app.run(debug=True)


