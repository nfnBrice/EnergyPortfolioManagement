#IMPORT FLASK
from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session
from flask import redirect
import string
import requests
import optimiz as optimiz
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
	
@app.route("/projects")
def project():
    return render_template('projects.html')	

@app.route("/showCreatePortfolio")
def showCreatePortfolio():
    return render_template('createPortfolio.html')

#page de tutoriel à faire avant cette page la 
@app.route('/createPortfolio', methods=['POST','GET'])
def createPortfolio():
	#create mysql connection
	conn = mysql.connect()
	#create cursor
	cursor = conn.cursor()
	try: 
		# read the posted values from the UI
		_amount = request.form['inputAmount']
		_horizon = request.form['inputHorizon']
		_knowledge = request.form['inputKnowledge']

		# validate the received values
		if _amount and _horizon and _knowledge:
			if _knowledge is 0:
				return render_template('tutorial.html')
			else :
				#find portfolio 
				cursor.callproc('sp_createPortfolio', (_amount, _horizon, session['user']))
				data = cursor.fetchall()
				print(data);
				if len(data) is 0:
					return json.dumps({'error':str(data[0])})
				else:
					conn.commit()
					session['portfolio'] = data[0][0] 
					return redirect('/showAddStocks')

		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	#except Exception as e:
	#	return json.dumps({'error':str(e)})
	finally:
		cursor.close() 
		conn.close()

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
			cursor.callproc('sp_createUser',(_email,_name,_hashed_password))
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
def signIn():
	try:
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_connect', (_email,)) #for some weird reason email is not one element but the number of char it is composed of 
		data = cursor.fetchall()
		
		if len(data) > 0:
			session['user'] = data[0][0]
			if check_password_hash(str(data[0][3]),_password):
				session['user'] = data[0][0]
				return redirect('/showCreatePortfolio')
			else:
				return render_template('error.html',error = 'Wrong Email address or Password.')
		else:
			#return render_template('error.html',error = 'caca')
			return render_template('index.html')

	except Exception as e:
		return render_template('error.html',error = str(e))	

	finally:
		cursor.close() 
		conn.close()	

@app.route('/showAddStocks')
def showStocks():
	try:
		#create mysql connection
		conn = mysql.connect()
		#create cursor
		cursor = conn.cursor()
		cursor.callproc('sp_getAllStocks', ())
		data = cursor.fetchall()
		return render_template('addStocks.html', data=data)
	except Exception as e:
		return render_template('error.html',error = str(e))	
		
	finally:
		cursor.close() 
		conn.close()

@app.route('/showTest')
def showTest():
	try: 
		#create mysql connection
		conn = mysql.connect()
		#create cursor
		cursor = conn.cursor()
		cursor.callproc('sp_getStocksbyID', ())
		data = cursor.fetchall()
		print(data)
		return render_template('addStocks.html', data=data)

	except Exception as e:
		return render_template('error.html',error = str(e))	
		
	finally:
		cursor.close() 
		conn.close()

#add Bonds to the portfolio
@app.route('/addStocks',methods=['POST'])


def addStocks():
	conn = mysql.connect()
	#create cursor
	cursor = conn.cursor()
	try:
		_a=10;
		_b=10;
		f = request.form
		for key in f.keys():
			_keyInt=int(key)
			cursor.callproc('sp_linkStockToPortfolio', (_a,_b,session['portfolio'], _keyInt))
			caca = cursor.fetchall()
			print(caca)
		return redirect('/showTest')
		
	finally:
		cursor.close() 
		conn.close()


#debug mode -> put to false when dev mode is finished
if __name__ == '__main__':
	app.run(debug=True, port=5002)