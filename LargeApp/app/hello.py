#IMPORT FLASK
from flask import Flask, render_template
app = Flask(__name__)


#WEBPAGES INITIALISATION 
#home webpage init
@app.route('/')
def home():
    return render_template('home.html')
#about webpage init 
@app.route('/about/')
def about():
    return render_template('about.html')


#debug mode -> put to false when dev mode is finished
if __name__ == '__main__':
    app.run(debug=True)