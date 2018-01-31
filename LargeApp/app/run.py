from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('createPortfolio.html')

@app.route("/signUp")
def	userHome():
	    return render_template('addStocks.html')

@app.route("/login")
def	signIn():
	    return render_template('login.html')

@app.route("/projects")
def project():
    return render_template('projects.html')

if __name__ == "__main__":
    app.run()
