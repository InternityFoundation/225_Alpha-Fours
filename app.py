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



