from flask import Flask, render_template, request, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
from decimal import Decimal
import threading
import time
import mysql.connector
import json

application = Flask(__name__, static_url_path='/static')
CORS(application)
#app = Flask(__name__)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)

application.json_encoder = CustomJSONEncoder

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

    json_list = []
    
    for result in myresult:
        data_dict = {
            "driverId": result[1],
            "date": result[2].strftime('%Y-%m-%d %H:%M:%S'),
            "speed": result[3]
        }
        json_list.append(data_dict)
        
    return jsonify(json_list)

start_datetime = datetime.strptime("2017-01-01 08:00:00", "%Y-%m-%d %H:%M:%S")
end_datetime = start_datetime + timedelta(seconds=30)

def update_datetime():
    global start_datetime, end_datetime
    while True:
        start_datetime += timedelta(seconds=30)
        end_datetime += timedelta(seconds=30)
        time.sleep(30)

update_thread = threading.Thread(target=update_datetime)
update_thread.daemon = True
update_thread.start()

@application.route('/car_speed_monitor', methods=['GET'])
def car_speed_monitor():
    global start_datetime, end_datetime

    mydb = db_connection()
    cur = mydb.cursor()

    sql_query = '''
        SELECT * FROM comp4442.DriverSpeedData
        WHERE CurrentTime BETWEEN %s AND %s
        ORDER BY CurrentTime
    '''

    cur.execute(sql_query, (start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
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
    start_datetime = datetime.strptime("2017-01-01 08:00:00", "%Y-%m-%d %H:%M:%S")
    global end_datetime
    mydb = db_connection()
    cur = mydb.cursor()
    sql_query = """
        SELECT 
            driverId,
            carPlateNumber,
            SUM(overspeedCount) as totalOverspeedCount,
            SUM(overspeedTotalTime) as overspeedTotalTimeCount,
            SUM(fatigueDrivingCount) as totalFatigueDrivingCount,
            SUM(oilLeakDrivingCount) as totalOilLeakDrivingCount,
            SUM(hthrottleStopCount) as totalHthrottleStopCount,
            SUM(neutralSlide_totalTime) as neutralSlideTotalTimeCount
        FROM 
            DriverStats
        WHERE 
            CurrentTime BETWEEN %s AND %s
        GROUP BY 
            driverId
    """
    
    cur.execute(sql_query, (start_datetime.strftime("%Y-%m-%d %H:%M:%S"), end_datetime.strftime("%Y-%m-%d %H:%M:%S")))
    
    myresult = cur.fetchall()
    json_list = []

    for result in myresult:
        data_dict = {
            "driverId": result[0],
            "carPlateNumber": result[1],
            "totalOverspeedCount": int(result[2]),
            "overspeedTotalTimeCount": int(result[3]),
            "totalFatigueDrivingCount": int(result[4]),
            "totalOilLeakDrivingCount": int(result[5]),
            "totalHthrottleStopCount": int(result[6]),
            "neutralSlideTotalTimeCount": int(result[7])
        }
        json_list.append(data_dict)
    
    return jsonify(json_list)

if __name__ == '__main__':
	application.run(port=5000, debug = True)




