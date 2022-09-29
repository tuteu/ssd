#Flaskとrender_template（HTMLを表示させるための関数）をインポート
import re
import sys
from flask import Flask, render_template, request,jsonify
from markupsafe import escape
import sqlite3
import json

#Flaskオブジェクトの生成
app = Flask(__name__)
dbname = r'C:\Users\tuteu\Desktop\RICO\new_teu\ForcedExcursionSystemV2-new_Runner-main\api\gateChecker.sqlite3'

app.config['JSON_AS_ASCII']=False
app.config['JSON_SORT_KEYS']=False


def get_event_department(event_id,department_id):
    
    '''
    cur1.execute('SELECT EventDepartment.id, Department.name FROM  EventDepartment\
     where EventDepartment.event_id='+str(event_id)+' AND EventDepartment.department_id='+str(department_id),
     'inner join Department ON Department.id=EventDepartment.id')

     cur.execute('SELECT Department.name, EventDepartment.id FROM  EventDepartment \
    inner join Department ON Department.id=EventDepartment.id',
    'EventDepartment where EventDepartment.event_id='+str(event_id)+' AND EventDepartment.department_id='+str(department_id))

cur.execute('SELECT \
                        Department.name,  \
                        EventDepartment.id  \
                FROM Department, \
    EventDepartment \
    where EventDepartment.event_id='+str(event_id)+' AND EventDepartment.department_id='+str(department_id))

        event_idとdepartment_idからevent_departmentの情報を検索する
        {'id':1 , 'department__name': "全日男子"} のような辞書オブジェクトが返る
    '''
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('SELECT Department.id,Department.name FROM \
     Department inner join  EventDepartment on Department.id=EventDepartment.id\
     where EventDepartment.event_id='+str(event_id)+' AND EventDepartment.department_id='+str(department_id))

    v_event_dep = cur.fetchall()
    result = None
    for event_dep in v_event_dep: # 1個しかないはず
        result = event_dep
    return result

#re=get_event_department(2,4)
#print(re)
 
def get_course_layout(department_id, gate_id=None):
    ''' 引数で指定された情報に対応する部門の関門情報（コースレイアウトを含む）を配列にして返す。
        gate_idをNoneにすると、その部門のコース全部を返す。指定すると指定された関門の情報だけ返す。
        空配列が返ったらID指定が間違っている。
    '''
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    a='SELECT CourseLayout.gate_id,Gate.name,CourseLayout.gateOrder,CourseLayout.distance FROM \
     CourseLayout inner join  Gate on CourseLayout.gate_id=Gate.id'
    results = []
    if gate_id == None:
        courses = cur.execute(a+' where CourseLayout.department_id=' + str(department_id))
    else:
        courses = cur.execute(a+' where CourseLayout.department_id=' + str(department_id)
         +' and  CourseLayout.gate_id=' + str(gate_id))
    v_event_dep = cur.fetchall()


    for course in v_event_dep:
        results.append({"id":course[0], "gateOrder":course[2], "name":course[1], "distance":course[3]})
    return results

re=get_course_layout(2)
print(re)


