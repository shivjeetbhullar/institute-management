from flask import Blueprint,render_template,request,redirect,session,flash,url_for
from quotes import Quotes
from threading import Timer
from datetime import datetime
from Web import db
from functools import wraps
from .functions import attendance,do_process
qt = Quotes()
mod = Blueprint('admin',__name__,template_folder='templates',static_folder='./static',static_url_path='/static/cdn/')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('admin.do_admin_login'))
    return wrap

@mod.route('/login/', methods=['POST',"GET"])
def do_admin_login():
 if request.method == "POST":
  if request.form['password'] == 'shivjeet' and request.form['username'] == 'Shivjeet':
    session['logged_in'] = True
    return redirect("/admin/")
  else:
    flash("Check Password Or Username!")
    return redirect(url_for('admin.do_admin_login'))
 else:
   if 'logged_in' in session:return redirect("/admin/")
   else:return render_template("admin_login.html")

@mod.route("/logout")
@login_required
def logout():
 session['logged_in'] = False
 session.clear()
 return do_admin_login()

@mod.route("/read/<col>")
@login_required
def logoutfd(col):
 return str(db.read(col))

@mod.route('/',methods = ['GET'])
@login_required
def admin_index():
    return render_template('admin_index.html',qut=qt.random(),students=len(db.read('students')['data']))

@mod.route('/insert',methods = ['GET','POST'])
@login_required
def admin_insert():
    if request.method == "POST":
        data = request.form.to_dict()
        db.write('students',data)
        return render_template('admin_insert.html',qut=qt.random(),stdwrit='True')
    else:return render_template('admin_insert.html',qut=qt.random())

@mod.route('/insertold',methods = ['GET','POST'])
@login_required
def admin_insertold():
    if request.method == "POST":
        data = request.form.to_dict()
        db.write('students',do_process(data))
        return render_template('admin_insertold.html',qut=qt.random(),stdwrit='True',exams=db.status()['exams'])
    else:return render_template('admin_insertold.html',qut=qt.random(),exams=db.status()['exams'])

@mod.route('/delstudent/<unid>',methods = ['GET'])
@login_required
def admin_delstudent(unid):
    db.trash('students',where={"unid":unid})
    return render_template('admin_results.html',qut=qt.random(),students = db.read("students"))

@mod.route('/result',methods = ['GET','POST'])
@login_required
def admin_result():
    if request.method == "POST":
        print(db.filter("students",request.form)['data'][0])
        return db.filter("students",request.form)['data'][0]
    else:return render_template('admin_results.html',qut=qt.random(),students = db.read("students"))

@mod.route('/exam/<req>',methods = ['GET'])
@mod.route('/exam',methods = ['GET','POST'])
@login_required
def admin_exam(req=None):
  if req is not None:
      return db.read('exams',request.args['name'])['data'][0]
  else:
    if request.method == "POST":
        db.write("exams",request.form['name'],{"data":[]})
        return render_template('admin_exam.html',qut=qt.random(),exams=db.status())
    return render_template('admin_exam.html',qut=qt.random(),exams=db.status())

@mod.route('/question/<query>',methods = ['GET','POST'])
@login_required
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
@login_required
def admin_attendance():
    if request.method == 'POST':
        if request.form['status'] == 'end':
            db.update("students",{'end':request.form['date']},where={'unid':request.form['unid']})
            return "Student Session Ended!"
        else:
            db.update("students",{'attendance':{request.form['date']:request.form['status']}},where={'unid':request.form['unid']})
            return "Absent Marked!"
    elif request.method == 'GET':return render_template('admin_attendance.html',qut=qt.random(),students = db.read("students"))

attendance()