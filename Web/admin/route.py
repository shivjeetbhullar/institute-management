from flask import Blueprint,render_template,request
from quotes import Quotes
from Web import db
qt = Quotes()
mod = Blueprint('admin',__name__,template_folder='templates',static_folder='./static',static_url_path='/static/cdn/')

@mod.route('/',methods = ['GET'])
def admin_index():
    return render_template('admin_index.html',qut=qt.random())

@mod.route('/insert',methods = ['GET','POST'])
def admin_insert():
    if request.method == "POST":
        db.write('students',request.form)
        return render_template('admin_insert.html',qut=qt.random())
    else:return render_template('admin_insert.html',qut=qt.random())

@mod.route('/delstudent/<unid>',methods = ['GET'])
def admin_delstudent(unid):
    db.trash('students',where={"unid":unid})
    return render_template('admin_results.html',qut=qt.random(),students = db.read("students"))

@mod.route('/result',methods = ['GET','POST'])
def admin_result():
    if request.method == "POST":return db.filter("students",request.form)['data'][0]
    return render_template('admin_results.html',qut=qt.random(),students = db.read("students"))

@mod.route('/attendance',methods = ['GET','POST'])
def admin_attendance():
    return render_template('admin_attendance.html',qut=qt.random(),students = db.read("students"))
