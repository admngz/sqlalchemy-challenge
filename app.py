# import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


# create an app
app = Flask(__name__)


# static routes
@app.route("/")
def home():
    return (f"Surf's Up API!</br></br>"
            f"Available Routes:</br></br>"
            f"/api/v1.0/stations</br>"
            f"/api/v1.0/precipitation</br>"
            f"/api/v1.0/tobs</br>")


@app.route("/api/v1.0/stations")
def stations():
    name = session.query(Station.name).all()
    all = list(np.ravel(name))
    return jsonify(all)
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()

    prcplist=[]

    for result in prcp:
        dict = {'Station':result.station, "Date":result.date, "Precipitation":result.prcp}
        # dict['station'] = result[0]
        # dict["date"] = result[1]
        # dict['prcp'] = result[2]
        prcplist.append(dict)
    return jsonify(prcplist)


@app.route("/api/v1.0/tobs")
def temp():
    tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date.desc()).all()

    templist=[]

    for result in tobs:
        dict = {'Station':result.station, "Date":result.date, "Temperature":result.tobs}
        templist.append(dict)
    return jsonify(templist)

#  main behavior
if __name__ == "__main__":
    app.run(debug=True)