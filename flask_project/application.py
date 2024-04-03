from flask import Flask, render_template, request
import mysql.connector
import os
import requests
import boto3

application = Flask(__name__, static_url_path='/static')
#app = Flask(__name__)

@application.route('/')
def new_student():
	return render_template('student.html')

def db_connection():
	mydb = mysql.connector.connect( host = 'database-1.clsosmgiicni.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442',
	passwd = '12345678')

	#print("successfully connect to the database")
	
	return mydb

def create_table():
    mydb = db_connection()
    cur = mydb.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS DriverStats (
			driverId INT,
			carPlateNumber VARCHAR(255),
			overspeedCount INT,
			overspeedTotalTime VARCHAR(255),
			fatigueDrivingCount INT,
			oilLeakDrivingCount INT,
			hthrottleStopCount INT,
			neutralSlide_totalTime VARCHAR(255)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS DriverSpeedData (
			ID INT,
			DriverID VARCHAR(255),
			CurrentTime INT,
			Speed INT,
			IsOverspeed BOOLEAN
        );
    """)
    mydb.commit()
    mydb.close()
	
@application.route('/list')
def list():
	mydb = db_connection()

	cur = mydb.cursor()
	cur.execute("select * from Students")

	myresult = cur.fetchall()
	for result in myresult:
		print(result)

	return render_template("list.html", results = myresult)

@application.route('/add_drive_plate_data')
def add_drive_plate_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/DrivePlate/part-00000', './output/DrivePlate/part-00001']
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                driver_id = parts[0].strip("('")
                car_plate_number = parts[1].strip(" ')").replace("'", "")

                cur.execute("SELECT COUNT(*) FROM DriverStats WHERE driverId = %s", (driver_id,))
                result = cur.fetchone()
                if result[0] > 0:
                    sql_update = "UPDATE DriverStats SET carPlateNumber = %s WHERE driverId = %s"
                    cur.execute(sql_update, (car_plate_number, driver_id))
                else:
                    sql = "INSERT INTO DriverStats (driverId, carPlateNumber) VALUES (%s, %s)"
                    val = (driver_id, car_plate_number)
                    cur.execute(sql, val)

                print(f"Driver ID: {driver_id}, Car Plate Number: {car_plate_number}")

    mydb.commit()
    mydb.close()

    return "Data successfully added from DrivePlate files"

@application.route('/add_fatigue_count_data')
def add_fatigue_count_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/FatigueCount/part-00000', './output/FatigueCount/part-00001']
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                driver_id = data[0].strip("('")
                fatigue_count = int(data[1].strip(")"))

                cur.execute("SELECT COUNT(*) FROM DriverStats WHERE driverId = %s", (driver_id,))
                result = cur.fetchone()
                if result[0] > 0:
                    sql_update = "UPDATE DriverStats SET fatigueDrivingCount = %s WHERE driverId = %s"
                    cur.execute(sql_update, (fatigue_count, driver_id))
                else:
                    sql_driver_stats = "INSERT INTO DriverStats (driverId, fatigueDrivingCount) VALUES (%s, %s)"
                    val_driver_stats = (driver_id, fatigue_count)
                    cur.execute(sql_driver_stats, val_driver_stats)

                print(f"Driver ID: {driver_id}, Fatigue Count: {fatigue_count}")

    mydb.commit()
    mydb.close()

    return "Data successfully updated in DriverStats from FatigueCount files"

@application.route('/add_hthrottle_stop_data')
def add_hthrottle_stop_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/HthrottleStop/part-00000', './output/HthrottleStop/part-00001']
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                driver_id = data[0].strip("('")
                hthrottle_stop_count = int(data[1].strip(")"))

                cur.execute("SELECT COUNT(*) FROM DriverStats WHERE driverId = %s", (driver_id,))
                result = cur.fetchone()
                if result[0] > 0:
                    sql_update = "UPDATE DriverStats SET hthrottleStopCount = %s WHERE driverId = %s"
                    cur.execute(sql_update, (hthrottle_stop_count, driver_id))
                else:
                    sql_driver_stats = "INSERT INTO DriverStats (driverId, hthrottleStopCount) VALUES (%s, %s)"
                    val_driver_stats = (driver_id, hthrottle_stop_count)
                    cur.execute(sql_driver_stats, val_driver_stats)
                    
                print(f"Driver ID: {driver_id}, Hthrottle Stop Count: {hthrottle_stop_count}")

    mydb.commit()
    mydb.close()

    return "Data successfully updated in DriverStats from HthrottleStop files"

@application.route('/add_neutral_slide_total_time_data')
def add_neutral_slide_total_time_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/NeutralSlideTotalTime/part-00000', './output/NeutralSlideTotalTime/part-00001']
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                driver_id = data[0].strip("('")
                neutral_slide_total_time = int(data[1].strip(")"))

                cur.execute("SELECT COUNT(*) FROM DriverStats WHERE driverId = %s", (driver_id,))
                result = cur.fetchone()
                if result[0] > 0:
                    sql_update = "UPDATE DriverStats SET neutralSlide_totalTime = %s WHERE driverId = %s"
                    cur.execute(sql_update, (neutral_slide_total_time, driver_id))
                else:
                    sql_driver_stats = "INSERT INTO DriverStats (driverId, neutralSlide_totalTime) VALUES (%s, %s)"
                    val_driver_stats = (driver_id, neutral_slide_total_time)
                    cur.execute(sql_driver_stats, val_driver_stats)
                    
                print(f"Driver ID: {driver_id}, Neutral Slide Total Time: {neutral_slide_total_time}")

    mydb.commit()
    mydb.close()

    return "Data successfully updated in DriverStats from NeutralSlideTotalTime files"

@application.route('/add_oil_leak_count_data')
def add_oil_leak_count_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/OilLeakCount/part-00000', './output/OilLeakCount/part-00001']
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                driver_id = data[0].strip("('")
                oil_leak_count = int(data[1].strip(")"))

                cur.execute("SELECT COUNT(*) FROM DriverStats WHERE driverId = %s", (driver_id,))
                result = cur.fetchone()
                if result[0] > 0:
                    sql_update = "UPDATE DriverStats SET oilLeakDrivingCount = %s WHERE driverId = %s"
                    cur.execute(sql_update, (oil_leak_count, driver_id))
                    print(f"Driver ID {driver_id} already exists, updating oilLeakDrivingCount")
                else:
                    sql_driver_stats = "INSERT INTO DriverStats (driverId, oilLeakDrivingCount) VALUES (%s, %s)"
                    val_driver_stats = (driver_id, oil_leak_count)
                    cur.execute(sql_driver_stats, val_driver_stats)
                    
                print(f"Driver ID: {driver_id}, Oil Leak Count: {oil_leak_count}")

    mydb.commit()
    mydb.close()

    return "Data successfully updated in DriverStats from OilLeakCount files"

@application.route('/add_overspeed_count_data')
def add_overspeed_count_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/OverspeedCount/part-00000', './output/OverspeedCount/part-00001']
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                driver_id = data[0].strip("('")
                overspeed_count = int(data[1].strip(")"))

                cur.execute("SELECT COUNT(*) FROM DriverStats WHERE driverId = %s", (driver_id,))
                result = cur.fetchone()
                if result[0] > 0:
                    sql_update = "UPDATE DriverStats SET overspeedCount = %s WHERE driverId = %s"
                    cur.execute(sql_update, (overspeed_count, driver_id))
                else:
                    sql_driver_stats = "INSERT INTO DriverStats (driverId, overspeedCount) VALUES (%s, %s)"
                    val_driver_stats = (driver_id, overspeed_count)
                    cur.execute(sql_driver_stats, val_driver_stats)

                print(f"Driver ID: {driver_id}, Overspeed Count: {overspeed_count}")

    mydb.commit()
    mydb.close()

    return "Data successfully updated in DriverStats from OverspeedCount files"

@application.route('/add_overspeed_total_time_data')
def add_overspeed_total_time_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/OverspeedTotalTime/part-00000', './output/OverspeedTotalTime/part-00001']
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                driver_id = data[0].strip("('")
                overspeed_total_time = int(data[1].strip(")"))

                cur.execute("SELECT COUNT(*) FROM DriverStats WHERE driverId = %s", (driver_id,))
                result = cur.fetchone()
                if result[0] > 0:
                    sql_update = "UPDATE DriverStats SET overspeedTotalTime = %s WHERE driverId = %s"
                    cur.execute(sql_update, (overspeed_total_time, driver_id))
                else:
                    sql_driver_stats = "INSERT INTO DriverStats (driverId, overspeedTotalTime) VALUES (%s, %s)"
                    val_driver_stats = (driver_id, overspeed_total_time)
                    cur.execute(sql_driver_stats, val_driver_stats)
                    
                print(f"Driver ID: {driver_id}, Overspeed Total Time: {overspeed_total_time}")

    mydb.commit()
    mydb.close()

    return "Data successfully updated in DriverStats from OverspeedTotalTime files"

@application.route('/add_driver_speed_data')
def add_driver_speed_data():
    mydb = db_connection()
    cur = mydb.cursor()

    filenames = ['./output/DriveSpeed/part-00000', './output/DriveSpeed/part-00001']
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                driver_id = data[0].strip("('")
                # Remove single quotes and carriage return from CurrentTime
                current_time_full = data[1].strip("'").replace("'", "")
                speed = int(data[2].strip(" '"))
                is_overspeed = int(data[3].strip(")"))

                # Insert new record into DriverSpeedData table
                sql_insert = "INSERT INTO DriverSpeedData (DriverID, CurrentTime, Speed, IsOverspeed) VALUES (%s, %s, %s, %s)"
                val_insert = (driver_id, current_time_full, speed, is_overspeed)
                cur.execute(sql_insert, val_insert)
                print(f"Driver ID: {driver_id}, Current Time: {current_time_full}, Speed: {speed}, Is Overspeed: {is_overspeed}")

    mydb.commit()
    mydb.close()

    return "Data successfully added to DriverSpeedData from DriveSpeed files"

if __name__ == '__main__':
    create_table()
    application.run(port=5000, debug=True)



