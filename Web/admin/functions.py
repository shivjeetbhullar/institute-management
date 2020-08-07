from threading import Timer
from datetime import datetime
from Web import db

def attendance():
    x=datetime.today()
    secs=(x.replace(day=x.day, hour=9, minute=0, second=0, microsecond=0)-datetime.today()).seconds
    if secs.days == -1:secs=(x.replace(day=x.day+1, hour=9, minute=0, second=0, microsecond=0)-datetime.today()).seconds
    task = Timer(secs, do_auto_attendance)
    task.start()

def do_auto_attendance():
    unids = db.readkey('students',key=['unid','end'])['data']
    for x in unids:
     if not 'end' in x:
      db.update("students",{'attendance':{datetime.now().strftime("%Y-%m-%d"):"Present"}},where={'unid':x['unid']})
    attendance()