#IMPORT FLASK
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session
from flask import redirect
import string
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'


#data base configuration 
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ma_base'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dayenu:secret.word@localhost/dayenu?unix_socket=/usr/local/mysql5/mysqld.sock'

mysql.init_app(app)

#WEBPAGES INITIALISATION 
#home webpage init
@app.route('/')
def main():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/showSignIn')
def showSignin():
	return render_template('signin.html')

@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/', code=302)

#signup procedure
@app.route('/signUp', methods=['POST','GET'])
def signUp():
	#create mysql connection
	conn = mysql.connect()
	#create cursor
	cursor = conn.cursor()
	try: 
		# read the posted values from the UI
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		# validate the received values
		if _name and _email and _password:
			#password generation
			_hashed_password = generate_password_hash(_password)
			#call the procedure create user 
			cursor.callproc('sp_createUser',(_name,_email,_password))
			#test to know if the data was well created 
			data = cursor.fetchall()
			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close() 
		conn.close()

#SignIn procedure
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
	try:
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		
		con = mysql.connect()
		cursor = con.cursor()
		cursor.callproc('sp_connect', _email) #for some weird reason email is not one element but the number of char it is composed of 
		data = cursor.fetchall()

		if len(data) > 0:

			if check_password_hash(str(data[0][3]),_password):
				session['user'] = data[0][0]
				return redirect('/userHome')
			else:
				return render_template('error.html',error = 'Wrong Email address or Password.')
		else:
			return render_template('error.html',error = 'caca')

	except Exception as e:
		return render_template('error.html',error = str(e))	

#debug mode -> put to false when dev mode is finished
if __name__ == '__main__':
	app.run(debug=True, port=5002)