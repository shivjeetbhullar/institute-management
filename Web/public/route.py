from flask import Blueprint,render_template,request

mod = Blueprint('public',__name__,template_folder='./templates',static_folder='./static',static_url_path='/static/cdn/')

@mod.route('/',methods = ['GET'])
def public_index():
    return render_template('index.html')

@mod.route('/exam',methods = ['GET'])
def public_exam():
    return render_template('exam.html')
