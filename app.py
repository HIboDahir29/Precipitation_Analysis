
# Import Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, date, time
import datetime as dt
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify

# ***********-------************

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

# ***********-------************

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


# ***********-------************

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

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
  # output in json list
    return jsonify(precipitation_data)


# ***********-------************

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # create session from Python DB
    session = Session(engine)

    # Query all stations data
    results = session.query(Station.station, Station.name).all()

    session.close()

    stations_data = []
    for station, name in results:
        station_dict = {}
        station_dict['Station ID'] = station
        station_dict['Station Name'] = name
        stations_data.append(station_dict)
  # output in json list
    return jsonify(stations_data)

# Query the dates and temperature observations
# of the most active station for the last year of data.


# ***********-------************

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session from Python DB
    session = Session(engine)

    Latest_date = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()
    # print(Latest_date)
    One_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   # query all the tobs data
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= One_year_ago).all()

    session.close()

    temperature_data = []
    for date, tobs in results:

        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
        temperature_data.append(temp_dict)

  # output in json list
    return jsonify(temperature_data)


# ***********-------************

# calculate TMIN, TAVG, and TMAX for all dates greater
#  than and equal to the start date.

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)
    # query all the start date data
    temperature = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()

    session.close()

    start_date_list = []
    for x in temperature:
        start_date_dict = {}
        start_date_dict['Date'] = x[0]
        start_date_dict['Tmin'] = x[1]
        start_date_dict['Tavg'] = round(x[2], 2)
        start_date_dict['Tmax'] = x[3]
        start_date_list.append(start_date_dict)

    # output in json list
    return jsonify(start_date_list)


# ***********-------************

# calculate the TMIN, TAVG, and
# TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)
    # query all the start to end date data
    temperature = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(
            Measurement.date <= end).group_by(Measurement.date).all()

    session.close()

    end_date_list = []
    for x in temperature:
        end_date_dict = {}
        end_date_dict['Date'] = x[0]
        end_date_dict['Tmin'] = x[1]
        end_date_dict['Tavg'] = round(x[2], 2)
        end_date_dict['Tmax'] = x[3]
        end_date_list.append(end_date_dict)

    # output in json list
    return jsonify(end_date_list)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
