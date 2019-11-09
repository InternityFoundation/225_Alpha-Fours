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

def result(dict1, dict2):
    weights = [2, 0, 2, 2, 3, 4, 3, 4, 4, 5]
    polarity_score = []
    subjectivity_score = 0

    for j in range(len(dict2[1])):
        polarity_score.append(dict2[1][j][0])
        subjectivity_score+=dict2[1][j][1]

    total_score=[a*b for a,b in zip(polarity_score,weights)]
    text_score=sum(total_score)/len(total_score)
    subjectivity_score=subjectivity_score/len(total_score)
    print("POLARITY SCORE",text_score)
    empath_dict={}
    
    for i in range(len(dict2[0])):
        for j in dict2[0][i]:
            if(j in empath_dict):
                empath_dict[j]+=dict2[0][i][j]
            else:
                empath_dict[j]=dict2[0][i][j]

    for i in empath_dict:
        if(i not in ['cheerfulness','pride','celebration','heroic','optmism']):
            empath_dict[i]*=-1

    empath_score=0
     
    for i in empath_dict:
         empath_score+=empath_dict[i]
         

    empath_score = empath_score/len(dict2[0])
    empath_score = empath_score/10

    print("EMPATH SCORE",empath_score)

    dict11={}
    for i in dict1[0]:
        print("running----------------------------------------")
        if(i=="angry"):
            dict11[i]=(dict1[0][i]*(-0.4))/dict1[1]
        elif(i=="happy"):
            dict11[i]=(dict1[0][i]*(1))/dict1[1]
        elif(i=="neutral"):
            dict11[i]=(dict1[0][i]*(0))/dict1[1]
        elif(i=="disgust"):
            dict11[i]=(dict1[0][i]*(0.1))/dict1[1] 
        elif(i=="surprised"):
            dict11[i]=(dict1[0][i]*(0.2))/dict1[1]
        elif(i=="sad"):
            dict11[i]=(dict1[0][i]*(-1))/dict1[1]
        else:
            dict11[i]=(dict1[0][i]*(-0.6))/dict1[1]
    print(dict11)
    print(dict1[1])
    video_score=0
    for i in dict11:
        video_score+=dict11[i]
    video_score=video_score/7
    print("VIDEO SCORE",video_score)
    total_final_score=(0.6*text_score)+(0.15*video_score)+(0.25*empath_score)
    
    gen=dict2[2];
    pause=sum(dict2[3])/len(dict2[3]);
    ros=sum(dict2[4])/len(dict2[4]);
    strr=dict2[5];
    str1="good"

    print("TOTAL SCORE:",total_final_score)
    print('GENDER ',dict2[2])
    print('PAUSES',sum(dict2[3])/len(dict2[3])) 
    print('RATE OF SPEECH',sum(dict2[4])/len(dict2[4]))  
    print('SPEAKING TIME RATIO',dict2[5]) 
    print("SUBJECTIVITY SCORE",subjectivity_score)

    if(total_final_score<-0.5):
        str1 = "Significantly distressed. Needs some improvement. Try to stay calm. "
        print(str1)
    elif(total_final_score>=-0.5 and total_final_score<0):
        str1 = "Moderately distressed. Freshen up your mind with positive thoughts. "
        print(str1)
    elif(total_final_score>=0 and total_final_score<0.5):
        str1 = "Stable state of mind. Cheer up yourself"
        print(str1)   
    else:
        str1 = "Well balanced state of mind. Cheer up yourself."
        print(str1)     
     