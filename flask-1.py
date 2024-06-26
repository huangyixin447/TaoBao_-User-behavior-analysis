from flask import Flask, redirect, url_for, request, abort, render_template
import json
from flask_cors import *
import calc
import threading as ts
import time


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html', hint = "")

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    inst = calc.StatisticClass()
    ret = inst.verfiylogin(username, password)
    if ret == 1:
        newdict = {'loginresult': 1}
        return json.dumps(newdict)
    elif ret == -1:
        newdict = {'loginresult': -1}
        return json.dumps(newdict)
    else:
        newdict = {'loginresult': -2}
        return json.dumps(newdict)



#     开始运算act_count
threadrun=None
@app.route('/show_act_count', methods=['GET', 'POST'])
def show_act_count():


    print('show_act_count')
    threadrun = ts.Thread(target=calc.running_act_count)
    threadrun.start()
    time.sleep(0.2)
    return json.dumps({})



#开始运算pv_count
@app.route('/show_pv_count',methods=['GET', 'POST'])
def show_pv_count():
    print('show_pv_count')
    threadrun = ts.Thread(target=calc.running_pv_top)
    threadrun.start()
    time.sleep(0.2)
    return  json.dumps({})


#开始运算buy_count
@app.route('/show_buy_count',methods=['GET', 'POST'])
def show_buy_count():
    print('show_buy_count')
    threadrun = ts.Thread(target=calc.running_buy_top)
    threadrun.start()
    time.sleep(0.2)
    return  json.dumps({})

#计算totalcount的值
@app.route("/run_total_count",methods=['GET', 'POST'])
def running ():
    print("run_total_count")
    threadrun = ts.Thread(target=calc.running_getTotalData)
    threadrun.start()
    time.sleep(0.2)

    return json.dumps({})




@app.route('/getdata',methods=['GET','post'])
def getData():
    print('getData')
    result=calc.getdata()
    newdict={
        'xdata':result[0],
        'ydata':result[1]
    }
    print(newdict)
    return json.dumps(newdict)


@app.route('/checkstatus',methods=['GET','POST'])
def checkStatus():
    print("checkStatus")
    isrunning,percentage=calc.checkStatus()
    newidc={
        'isrunning':isrunning,
        'percentage':percentage
    }
    print(newidc)
    return json.dumps(newidc)


@app.route('/table',methods=['GET','POST'])
def table():
    return  render_template("taobao.html")


@app.route('/get_Total_Count',methods=['GET','POST'])
def  get_Total_Count():
    result =calc.get_totaldata()

    return  json.dumps(result)


#获取time计算
@app.route('/time_action',methods=["GET","POST"])
def time_count():
    result1,result2=calc.time_work()
    print(result1)
    print(result2)
    return  json.dumps({
        "result1":result1,
        "result2":result2
    })



    
if __name__=="__main__":
    print('\n-------------\nflask is running')
    app.run(host='127.0.0.1', port =5001, debug=True, use_reloader=False)
