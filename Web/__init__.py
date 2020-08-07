from flask import Flask
from pi7db import pi7db

db = pi7db('Students','Web/DATABASE')
app = Flask(__name__)

from Web.public.route import mod
from Web.admin.route import mod

@app.route('/robots.txt/',methods = ['GET'])
@app.route('/robots.txt',methods = ['GET'])
def robots():
     response = make_response(open('robots.txt').read())
     response.headers["Content-type"] = "text/plain"
     return response

app.register_blueprint(public.route.mod,url_prefix='/')
app.register_blueprint(admin.route.mod,url_prefix='/admin')

app.secret_key = "#@&GodIsGreat!"