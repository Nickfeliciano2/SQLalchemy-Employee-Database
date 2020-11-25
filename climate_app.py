#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_
from sqlalchemy import distinct

from flask import Flask, jsonify

import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect = True)


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    q = session.query(Measurement.date, Measurement.prcp).filter(and_(Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23")).all()

    results_dict = {}
    for result in q:
        results_dict[result[0]] = result[1]

    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_query= session.query(Station.station, Station.name).all()
    station_list = list(station_query)
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
 
    temp_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281", Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23").all()

    top_station = list(temp_data)

    return jsonify(top_station)

@app.route("/api/v1.0/start/end")
def startend():

    temp_list = []

    min_temp = session.query(Measurement.station, func.min(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()

    max_temp = session.query(Measurement.station, func.max(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()

    avg_temp = session.query(Measurement.station, func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()

    temp_list.append(min_temp)

    temp_list.append(max_temp)

    temp_list.append(avg_temp)


    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug = True)