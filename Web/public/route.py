from flask import Blueprint,render_template,request
from Web import db
import json
mod = Blueprint('public',__name__,template_folder='./templates',static_folder='./static',static_url_path='/static/cdn/')

@mod.route('/',methods = ['GET'])
def public_index():
    return render_template('index.html')

@mod.route('/exam',methods = ['GET'])
def public_exam():
    return render_template('examlogin.html',exams=db.status()['exams'])

@mod.route('/submitresult',methods = ['POST'])
def public_submitresult():
    db.update("students",{'result':{request.form['exam']:request.form['result']}},where={'unid':request.form['unid']})
    return "Exam Is Submitted!"


@mod.route('/doexam',methods = ['POST'])
def public_doexam():
    data = db.filter('students',{'id':request.form['id']})['data']
    if len(data):
      return render_template('exam.html',data=data[0],que=json.dumps(db.read('exams',request.form['paper'])['data'][0]['data']),unid=data[0]['unid'],exam=request.form['paper'])
    else:return render_template('examlogin.html',exams=db.status()['exams'],msg='Student ID Incorrect!')
