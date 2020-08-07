from flask import Blueprint,render_template,request,redirect
from quotes import Quotes
from threading import Timer
from datetime import datetime
from Web import db
from .functions import attendance
qt = Quotes()
mod = Blueprint('admin',__name__,template_folder='templates',static_folder='./static',static_url_path='/static/cdn/')

@mod.route('/',methods = ['GET'])
def admin_index():
    return render_template('admin_index.html',qut=qt.random(),students=len(db.read('students')['data']))

@mod.route('/insert',methods = ['GET','POST'])
def admin_insert():
    if request.method == "POST":
        db.write('students',request.form)
        return render_template('admin_insert.html',qut=qt.random(),stdwrit='True')
    else:return render_template('admin_insert.html',qut=qt.random())

@mod.route('/delstudent/<unid>',methods = ['GET'])
def admin_delstudent(unid):
    db.trash('students',where={"unid":unid})
    return render_template('admin_results.html',qut=qt.random(),students = db.read("students"))

@mod.route('/result',methods = ['GET','POST'])
def admin_result():
    if request.method == "POST":return db.filter("students",request.form)['data'][0]
    return render_template('admin_results.html',qut=qt.random(),students = db.read("students"))

@mod.route('/exam/<req>',methods = ['GET'])
@mod.route('/exam',methods = ['GET','POST'])
def admin_exam(req=None):
  if req is not None:
      return db.read('exams',request.args['name'])['data'][0]
  else:
    if request.method == "POST":
        db.write("exams",request.form['name'],{"data":[]})
        return render_template('admin_exam.html',qut=qt.random(),exams=db.status())
    return render_template('admin_exam.html',qut=qt.random(),exams=db.status())

@mod.route('/question/<query>',methods = ['GET','POST'])
def admin_questions(query):
   if request.method == 'POST':
     db.trash("exams",request.form['exam'],{"data":[{'$keys':['que','choices'],'$where':{'que':request.form['que'].strip()}}]})
     return "True"
   else:
    if query == "add":
     data = request.args.to_dict()
     data['que']=data['que'].strip()
     data['choices'] = {
           'correct': data.pop('ans'),
           'wrong': data.pop('oans').split(',')
                      }
     db.update("exams",data.pop('exam'),{"data":[data]},append_list=True)
     return "True"
    

@mod.route('/attendance',methods = ['GET','POST'])
def admin_attendance():
    print(db.readkey('students',key=['unid','end'])['data'])
    if request.method == 'POST':
        if request.form['status'] == 'end':
            db.update("students",{'end':request.form['date']},where={'unid':request.form['unid']})
            return "Student Session Ended!"
        else:
            db.update("students",{'attendance':{request.form['date']:request.form['status']}},where={'unid':request.form['unid']})
            return "Absent Marked!"
    elif request.method == 'GET':return render_template('admin_attendance.html',qut=qt.random(),students = db.read("students"))


#attendance()