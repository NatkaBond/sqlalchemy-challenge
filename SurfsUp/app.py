# Import necessary libraries
from flask import Flask, jsonify

# Create an instance of Flask
app = Flask(__name__)

# Define routes
@app.route("/")
def homepage():
    return (
        f"Welcome to the Hawaii Weather API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert prcp_data_df to a dictionary with date as the key and prcp as the value
    precipitation_dict = prcp_data_df.to_dict()["Precipitation"]
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query list of stations
    stations_list = session.query(Station.station).all()
    stations = list(np.ravel(stations_list))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query temperature observations for the most active station in the last year
    temp_obs_last_year = session.query(Measurement.date, Measurement.tobs).\
                          filter(Measurement.station == most_active_station).\
                          filter(Measurement.date >= one_year_ago).all()
    return jsonify(temp_obs_last_year)

@app.route("/api/v1.0/<start>")
def temp_summary_start(start):
    # Calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    temp_summary = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                   filter(Measurement.date >= start).all()
    return jsonify(temp_summary)

@app.route("/api/v1.0/<start>/<end>")
def temp_summary_range(start, end):
    # Calculate TMIN, TAVG, and TMAX for dates between start and end (inclusive)
    temp_summary_range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                         filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp_summary_range)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)


