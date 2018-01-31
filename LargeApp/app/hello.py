#IMPORT FLASK
from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session
from flask import redirect
import string
import requests
import optimiz as optimiz
<<<<<<< HEAD
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

#data base configuration
=======
import pandas as pd
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

#data base configuration 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ma_base'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dayenu:secret.word@localhost/dayenu?unix_socket=/usr/local/mysql5/mysqld.sock'

mysql.init_app(app)

#WEBPAGES INITIALISATION
#home webpage init
@app.route('/')
def main():
	return render_template('index.html')

@app.route('/signUp')
def showSignUp():
	return render_template('signUp.html')

@app.route('/login')
def showSignin():
<<<<<<< HEAD
	return render_template('login.html')

@app.route("/projects")
def project():
    return render_template('projects.html')
=======
	return render_template('signin.html')
	
@app.route("/projects")
def project():
    return render_template('projects.html')	
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11

@app.route("/showCreatePortfolio")
def showCreatePortfolio():
    return render_template('createPortfolio.html')

<<<<<<< HEAD
#page de tutoriel à faire avant cette page la
=======
#page de tutoriel à faire avant cette page la 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
@app.route('/createPortfolio', methods=['POST','GET'])
def createPortfolio():
	#create mysql connection
	conn = mysql.connect()
	#create cursor
	cursor = conn.cursor()
<<<<<<< HEAD
	try:
=======
	try: 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
		# read the posted values from the UI
		_amount = request.form['inputAmount']
		_horizon = request.form['inputHorizon']
		_knowledge = request.form['inputKnowledge']

		# validate the received values
		if _amount and _horizon and _knowledge:
			if _knowledge is 0:
				return render_template('tutorial.html')
			else :
<<<<<<< HEAD
				#find portfolio
=======
				#find portfolio 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
				cursor.callproc('sp_createPortfolio', (_amount, _horizon, session['user']))
				data = cursor.fetchall()
				if len(data) is 0:
					return json.dumps({'error':str(data[0])})
				else:
					conn.commit()
<<<<<<< HEAD
					session['portfolio'] = data[0][0]
=======
					session['portfolio'] = data[0][0] 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
					return redirect('/showAddStocks')

		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	#except Exception as e:
	#	return json.dumps({'error':str(e)})
	finally:
<<<<<<< HEAD
		cursor.close()
=======
		cursor.close() 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
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
<<<<<<< HEAD
			#call the procedure create user
			cursor.callproc('sp_createUser',(_email,_name,_hashed_password))
			#test to know if the data was well created
=======
			#call the procedure create user 
			cursor.callproc('sp_createUser',(_email,_name,_hashed_password))
			#test to know if the data was well created 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
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
<<<<<<< HEAD

		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_connect', (_email,)) #for some weird reason email is not one element but the number of char it is composed of
=======
		
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_connect', (_email,)) #for some weird reason email is not one element but the number of char it is composed of 
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11
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
<<<<<<< HEAD

	except Exception as e:
		return render_template('error.html',error = str(e))

	finally:
		cursor.close()
		conn.close()
=======
>>>>>>> a7987be0e8d08ce4d501c0aa1959bfb800507b11

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
		f = request.form
		caca=[ ]

		for key in f.keys():
			session['key']=int(key);
			cursor.callproc('sp_linkStockToPortfolio', (session['portfolio'], session['key']))
			portfolioLinkAdded = cursor.fetchall()
			caca.append(portfolioLinkAdded[0][4])
			conn.commit()

		#print(caca)
		optimiz.optimiz(caca)

		return redirect('/showTest')

	finally:
		cursor.close()
		conn.close()


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

@app.route('/showPortfolio')
def showPortfolio():
	try: 
		#create mysql connection
		conn = mysql.connect()
		#create cursor
		cursor = conn.cursor()

		amountList=[ ]
		stocksOfCurrentPortfolio = [ ]
		cursor.callproc('sp_getLinkDataFromPortfolioID',(session['portfolio'],))
		data = cursor.fetchall()
		i=0
		for each in data:
			amountList.append(each[2])
			cursor.callproc('sp_getStockInfoFromLinkID',(each[4],))
			CurrentStocks = cursor.fetchall()
			#CurrentStocksdf = pd.DataFrame(CurrentStocks[0])
			stocksOfCurrentPortfolio.append(CurrentStocks[0])
			#stocksOfCurrentPortfolio[0].remove(stocksOfCurrentPortfolio[i][0])
			i=i+1
		df = pd.DataFrame(stocksOfCurrentPortfolio)
		df['amount'] = amountList
		df.rename(
            columns={0: 'id', 1: 'code', 2: 'name', 'amount': 'weight'},
            inplace=True
        )
		del df['id']
		return render_template('portfolio.html', data=df.to_html())
	#except Exception as e:
	# 	return render_template('error.html',error = str(e))	
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
		cursor.callproc('sp_getLinkDataFromPortfolioID', (session['portfolio'],))
		isThereLinksInPortfolio = cursor.fetchall()

		#if isThereLinksInPortfolio means the portfolio is full -> ask user to modify it or create a new one. 
		if(not isThereLinksInPortfolio):
			f = request.form
			caca=[ ]

			for key in f.keys():
				session['key']=int(key);
				cursor.callproc('sp_linkStockToPortfolio', (session['portfolio'], session['key']))
				portfolioLinkAdded = cursor.fetchall()
				caca.append(portfolioLinkAdded[0][4])
				conn.commit()

			#print(caca)
			optimiz.optimiz(caca)
		return redirect('/showPortfolio')
		
	finally:
		cursor.close() 
		conn.close()


#debug mode -> put to false when dev mode is finished
if __name__ == '__main__':
	app.run(debug=True, port=5002)
