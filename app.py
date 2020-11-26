
# Import Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify

# Setting up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Autoamp_base
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Initializing variables to save the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# setting up the flask app
app = Flask(__name__)

# Routes


@app.route("/")
def welcome():
    """Welcome! All available api routes."""
    return (
        f"List all available api routes:<br/>"
        f" <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


# # Route for percipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
  # Create our session (link) from Python to the DB
    session = Session(engine)

# Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
