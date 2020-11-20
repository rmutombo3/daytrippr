#import packages
from flask import Flask
from flask import render_template
from flask import flash
from flask import redirect, request, session, abort, send_from_directory, send_file, jsonify
from datetime import datetime
from datetime import timedelta
import re
import pandas as pd
import numpy as np
import json
import csv

#declare application
app = Flask(__name__)

# data store
class DataStore():
    StartingZip = None
    StartingLongitude = None
    StartingLatitude = None
    LeaveDate = None
    Adventure = None
    Rain = None
    Sun = None
    Wind = None
    DriveTime = None
    DTime = None
    EventType = None
    Address = None
    Description = None
    Narrative = None
    WindSpeed = None
    PrecipChance = None
    Filter = None
    DataFrame = None
data = DataStore()

#default route
@app.route("/",methods=["GET", "POST"])
def home():
    data.StartingZip = request.form.get("starting_zip")
    data.LeaveDate = request.form.get("leave_date")
    data.Adventure = request.form.get("adventure")
    data.Rain = request.form.get("rain")
    data.Sun = request.form.get("sun")
    data.Wind = request.form.get("wind")
    data.DriveTime = request.form.get("drive_time")
    data.DTime = request.form.get("dtime")

    #initialize
    starting_zip = data.StartingZip 
    leave_date = data.LeaveDate 
    event_type = data.Adventure
    drive_time = data.DriveTime
    dtime = data.DTime
    wind = data.Wind
    rain = data.Rain
    sun = data.Sun

    #read in data
    df = pd.read_csv("static/classified.csv")

    #populate event type dropdownbox
    adventure = []
    for index,row in df.iterrows():
         if row.event_type not in adventure:
             adventure.append((row.event_type))

    #handle postback
    if request.method == "POST":
        
        starting_zip = data.StartingZip
        if starting_zip == None:
              starting_zip = "30329"

        if leave_date == '':
            leave_date = '2020-11-20'

        if drive_time == None:
            drive_time = 5

        if dtime == '':
            dtime = 5
        
        if event_type == None:
            event_type == ''

        leave_date_split = leave_date.split('-')
        leave_date_modified = leave_date_split[1] + "/" + leave_date_split[2] + "/" + leave_date_split[0]
        df = df[df.start_date == leave_date_modified]

        filter = {"start_date": leave_date_modified, "event_type": event_type, 
        "drive_time": dtime, "rain": rain, "sun": sun, "wind": wind}

        data.Filter = filter

    return render_template("index.html", adventure=adventure)
 
@app.route("/get-filter",methods=["GET","POST"])
def getfilter():
    
    if data.Filter == None:
        data.Filter = {"start_date": "11/20/2020", "event_type": "", 
         "drive_time": 5, "rain": None, "sun": None, "wind": None}
    
    return data.Filter 

if __name__ == "__main__":
    app.run('localhost', 4449)
