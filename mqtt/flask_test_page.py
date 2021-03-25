# Link : https://flask.palletsprojects.com/en/1.1.x/quickstart/
import webbrowser

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

# launch flask web page 
webbrowser.open("http://localhost:5000", new=1)