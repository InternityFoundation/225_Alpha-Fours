from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import MySQLdb
from werkzeug.utils import secure_filename
import json
import os
import audio_record_analysis
import real_time_video
import sys
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'scb'
with open('config.json','r') as c:
    params = json.load(c)["params"]

dict1 = {}
dict2 = {}

def f1(dict1):
    r1, r2 = real_time_video.video_c()
    dict1[0] = r1  # single dictionary containing the values
    dict2[1] = r2  # the count of the number of iterations to normalize the values

def f2(dict2):
    r1, r2, r3, r4, r5, r6 = audio_record_analysis.audio_c_bot()
    try:
        os.chdir('audio_chunks')
        remove_all()
    except:
        print("cleaning complete")

    def remove_all():
        try:
            for i in range(0,5):
                file = "audio"+str(i)+".TextGrid"
                os.remove(file)
        except:
            pass
    dict2[0] = r1
    dict2[1] = r2
    dict2[2] = r3
    dict2[3] = r4
    dict2[4] = r5
    dict2[5] = r6

mydb = MySQL.connect(
    host = "localhost",
    user = "root",
    passwd = "admin",
    database = "smart_c_bot"
)

mycursor = mydb.cursor(MySQLdb.cursors.DictCursor)

@app.route("/")  # the first function to be called as soon as the application starts
def homepage():
    return render_template('homepage.html')

@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    if('user' in session):
        return render_template('dashboard.html')
    if(request.method == "POST"):
        username = request.form.get('uname')
        userpass = request.form.get('upass')

        sql_query = "select * from login_cred"
        mycursor.execute(sql_query)
        myresult = mycursor.fetchall()

        f = 0
        for x in myresult:
            if(x['username'] == username):
                if(x['password'] == userpass):
                    session['user'] = username
                    f = 1
                    break
        if(f == 1):
            return render_template('dashboard.html')
        else:
            return render_template('homepage.html')
    return render_template('homepage.html')

@app.route('/test')
def continuous():
    return render_template('testwindow.html')

@app.route('/start-test')
def test():  # using multi processing to run the video and audio analysis together
    manager = multiprocessing.Manager()
    dict1 = manager.dict()
    dict2 = manager.dict()
    proc1 = Process(target = f1,args = (dict1,))
    proc2 = Process(target = f2,args = (dict2,))

    proc2.join() # wait till video analysis sends in the dictionary file
    proc1.join() 

    while(len(list(dict2)) == 0):
        continue
    result(dict1, dict2)

    return "Report Sent"

@app.route('/logout')
def logout():
    session.pop('user')  # clearing the username stored in the session
    return redirect('/')

@app.route('/viewreports')
def viewreports():
    return  "Reports"


app.run(debug = True)
