from flask import Flask, render_template, request, jsonify
from datetime import datetime
import mysql.connector
import json

application = Flask(__name__, static_url_path='/static')
#app = Flask(__name__)

@application.route('/')
def new_student():
	return render_template('student.html')

@application.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		Name = request.form['Name']
		ID = request.form['ID']
		Department = request.form['Department']
		Email = request.form['Email']

		mydb = db_connection()
		cur = mydb.cursor()
		info = "insert into Students values('{}','{}','{}','{}')".format(Name, ID, Department, Email)
		cur.execute(info)

		mydb.commit()
		msg = "Record successfully added"

		mydb.close()
		return render_template("result.html",msg = msg)

def db_connection():
	mydb = mysql.connector.connect( host = 'database-1.clsosmgiicni.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442',
	passwd = '12345678')

	#print("successfully connect to the database")
	
	return mydb

@application.route('/car_speed_monitor', methods=['GET'])
def car_speed_monitor():
    mydb = db_connection()
    cur = mydb.cursor()

    # Convert time strings to datetime objects
    start_datetime = "2017-01-01 08:00:05"
    end_datetime = "2017-01-01 08:00:30"

    mydb = db_connection()
    cur = mydb.cursor()

    sql_query = '''
        SELECT * FROM comp4442.DriverSpeedData
        WHERE CurrentTime BETWEEN %s AND %s
        ORDER BY CurrentTime
    '''

    cur.execute(sql_query, (start_datetime, end_datetime))
    myresult = cur.fetchall()
    json_list = []

    for result in myresult:
        data_dict = {
            "ID": result[0],
            "DriverID": result[1],
            "CurrentTime": result[2],
            "Speed": result[3],
            "IsOverspeed": result[4]
        }
        json_list.append(data_dict)

    mydb.close()
    return jsonify(json_list)

@application.route('/summary', methods=['GET'])
def summary():
    mydb = db_connection()
    cur = mydb.cursor()
    sql_query = "select ds.driverId, \
                    ROUND(AVG(dsd.Speed), 1) AS `AVG Speed`, \
                    COUNT(dsd.isOverspeed) AS `Overspeed`, \
                    ds.carPlateNumber, \
                    ds.overspeedCount, \
                    ds.overspeedTotalTime, \
                    ds.fatigueDrivingCount, \
                    ds.oilLeakDrivingCount, \
                    ds.hthrottleStopCount, \
                    ds.neutralSlide_totalTime \
                from \
                    comp4442.DriverSpeedData dsd \
                join \
                    comp4442.DriverStats ds ON ds.driverId = dsd.driverId \
                group by \
                    ds.driverId, \
                    ds.carPlateNumber, \
                    ds.overspeedCount, \
                    ds.overspeedTotalTime, \
                    ds.fatigueDrivingCount, \
                    ds.oilLeakDrivingCount, \
                    ds.hthrottleStopCount, \
                    ds.neutralSlide_totalTime" 
    
    cur.execute(sql_query)
    
    myresult = cur.fetchall()
    json_list = []  # Create an empty list to hold the data dictionaries

    for result in myresult:
        data_dict = {
            "driverId": result[0],
            "avgSpeed": result[1],
            "overspeed": result[2],
            "carPlateNumber": result[3],
            "overspeedCount": result[4],
            "overspeedTotalTime": result[5],
            "fatigueDrivingCount": result[6],
            "oilLeakDrivingCount": result[7],
            "hthrottleStopCount": result[8],
            "neutralSlide_totalTime": result[9]
        }
        json_list.append(data_dict)  # Append each data dictionary to the list
    
    return jsonify(json_list)

@application.route('/overspeed_history', methods=['GET'])
def overspeed_history():
    mydb = db_connection()
    cur = mydb.cursor()
    
    sql_query = '''
                    select * from comp4442.DriverSpeedData where IsOverspeed = 1
                    order by DriverID, CurrentTime
                '''
    
    cur.execute(sql_query)

    myresult = cur.fetchall()

    json_list = []  # Create an empty list to hold the data dictionaries
    
    for result in myresult:
        data_dict = {
            "driverId": result[1],
            "date": result[2].strftime('%Y-%m-%d %H:%M:%S'),
            "speed": result[3]
        }
        json_list.append(data_dict)
        
    return jsonify(json_list)

if __name__ == '__main__':
	application.run(port=5000, debug = True)




