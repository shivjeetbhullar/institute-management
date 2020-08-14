from threading import Timer
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime,date,timedelta
import atexit,random,json
from Web import db

scheduler = BackgroundScheduler()

def attendance():
    scheduler.add_job(func=do_auto_attendance, trigger="interval", hours=24)
    scheduler.start()

def do_auto_attendance():
    if date.today().weekday() != 6:
     unids = db.readkey('students',key=['unid','end'])['data']
     for x in unids:
      if not 'end' in x:
       db.update("students",{'attendance':{date.today().strftime('%Y-%m-%d'):"Present"}},where={'unid':x['unid']})

def do_process(data):
    date = datetime.strptime(data['jdate'], '%Y-%m-%d').date()
    data['result'],data['attendance'] = {data['exam']:[]},{}
    exam = db.read('exams',data['exam'])['data'][0]['data']
    marks = int(len(exam)-int(data['marks'])/100*len(exam))
    for x in exam:
      i = random.randint(0,3)
      x['choices']['wrong'].insert(i,x['choices']['correct'])
      data['result'][data['exam']].append({"que":x['que'],"choices":x['choices']['wrong'],"user_choice_index":i,"correct_choice_index":i})
    
    while marks != 0:
        i = random.randint(0,len(data['result'][data['exam']])-1)
        popdata = data['result'][data['exam']].pop(i)
        if popdata['user_choice_index']!=0:popdata['user_choice_index'] -= 1
        else:popdata['user_choice_index'] += 1
        data['result'][data['exam']].insert(i,popdata)
        marks -= 1

    data['result'][data['exam']] = json.dumps(data['result'][data['exam']])
    print(datetime.strptime(data['edate'], '%Y-%m-%d').date() , date)
    while datetime.strptime(data['edate'], '%Y-%m-%d').date() > date:
     if date.weekday() != 6:
       data['attendance'][date.strftime('%Y-%m-%d')] = "Present"
       date += timedelta(days=1)
     else:date += timedelta(days=1)
    return data

atexit.register(lambda: scheduler.shutdown())
#APScheduler