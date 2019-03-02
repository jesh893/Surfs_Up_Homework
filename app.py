from flask import Flask, jsonify


#dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

import pandas as pd
import numpy as np
import datetime

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
	results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").group_by(Measurement.date).all()

	year_prcp = list(np.ravel(results))
	"""year_prcp = []
	for result in results:
		row = {}
		row[Measurement.date] = row[Measurement.prcp]
		year_prcp.append(row)"""

	return jsonify(year_prcp)

@app.route("/api/v1.0/stations")
def stations():
	results = session.query(Stations.station).all()
	all_stations = list(np.ravel(results))
	return jsonify(all_stations)

if __name__ == '__main__':
    app.run()
