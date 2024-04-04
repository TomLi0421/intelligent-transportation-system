from flask import Flask, render_template, request
import mysql.connector
import json
from decimal import Decimal

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

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

@application.route('/summary')
def summary():
	mydb = db_connection()
	cur = mydb.cursor()
	sql_query = "SELECT ds.driverId, \
    				ROUND(AVG(dsd.Speed), 1) AS `AVG Speed`, \
					COUNT(dsd.isOverspeed) AS `Overspeed`, \
					ds.carPlateNumber, \
					ds.overspeedCount, \
					ds.overspeedTotalTime, \
					ds.fatigueDrivingCount, \
					ds.oilLeakDrivingCount, \
					ds.hthrottleStopCount, \
					ds.neutralSlide_totalTime \
				FROM \
					comp4442.DriverSpeedData dsd \
				JOIN \
					comp4442.DriverStats ds ON ds.driverId = dsd.driverId \
				GROUP BY \
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
	
	json_data = json.dumps(json_list, cls=DecimalEncoder) # Convert the list to a JSON string

	return render_template("json.html", json_data=json_data)


@application.route('/car_speed_monitor')
def list():
	mydb = db_connection()
	cur = mydb.cursor()
	
	sql_query = '''
					SELECT DriverID, DATE(CurrentTime) AS `Date`, ROUND(AVG(Speed), 1) AS `AVG Speed`
	 				FROM comp4442.DriverSpeedData
	 				GROUP BY DriverID, DATE(CurrentTime)
	 				ORDER BY DriverID, Date
				'''
	
	cur.execute(sql_query)

	myresult = cur.fetchall()

	json_list = []  # Create an empty list to hold the data dictionaries
	
	for result in myresult:
		data_dict = {
			"driverId": result[0],
			"date": result[1].strftime('%Y-%m-%d'),
			"speed": result[2]
		}
		json_list.append(data_dict)
		
	json_data = json.dumps(json_list, cls=DecimalEncoder)  # Convert the list to a JSON string

	return render_template("json.html", json_data=json_data)


@application.route('/overspeed_history')
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
		
	json_data = json.dumps(json_list, cls=DecimalEncoder)  # Convert the list to a JSON string

	return render_template("json.html", json_data=json_data)


if __name__ == '__main__':
	application.run(port=5000, debug = True)




