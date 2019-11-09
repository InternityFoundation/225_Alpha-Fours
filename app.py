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





