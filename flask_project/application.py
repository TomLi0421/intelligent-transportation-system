from flask import Flask, render_template, request
import mysql.connector

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

@application.route('/list')
def list():
	mydb = db_connection()

	cur = mydb.cursor()
	cur.execute("select * from Students")

	myresult = cur.fetchall()
	for result in myresult:
		print(result)

	return render_template("list.html", results = myresult)

if __name__ == '__main__':
	application.run(port=5000, debug = True)




