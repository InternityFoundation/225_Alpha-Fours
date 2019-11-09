from gtts import gTTS
from playsound import playsound
import time
import speech_recognition as sr
import os
questions=[["Hi, thanks for coming in today.Think of me as a friend I do not judge people , I can not because  I am a computer.I will ask a few questions to get us started and please feel free to tell me anything , your answers are totally confidential.   So , how are you doing today? : "],
          ["where are you from : "],
          ["what are some cool things about the place you live : ",
          "what are somethings you really hate about the place you live in : ",
          "how do you feel about the place you live in : "],
          ["what do you do to relax : ",
          "what do you do when you feel tired out : ",
          "How often do you feel tired out for no good reason and what do you in that situation : "],
          ["what do you do when you are annoyed : ",
          "what do you when you fell restless and want to calm down : ",
          "How do you control your temper : "],
          ["when was the last time you argued with someone and what was it about : ",
          "how do you feel in the moment when you argue with somone : ",
          "How often do you indulge in a fight or argument with someone . Can you tell something about the last time you had a argument : "],
          ["who's someone that's been a positive influence in your life. Can you describe about it. : " ,
          "how close are you to your family and friends. : ",
          "What is the most memorable moment of your life that you had with your friends or family : "],
          ["In the past few days have you been so unhappy that you have been crying endlessly : ",
          "Did the thought of harming yourself ever occur to you and what was it for : ",
          "Did you ever scared or panicky for no very good reason in the past few days and why : "],
          ["Is there anything you regret : ",
          "Is the anything which bothers you again and again : " ,
          "Do you feel sad or miserable about something you did : "],
          ["have you ever been diagnosed with depression : ",
          "have you ever faced a situation which has caused a serious impact on your mental health : ",
          "How often do you feel down,depressed or hopeless : "]
           ]

describe=["Can you tell me something more about it",
          "Tell me more about it",
          "like what",
          "I didn't get you . Can you please elaborate"]

positive=["that is great",
         "awesome",
         "that is good",
         "nice",
         "yeah",
         "cool"]
         
neutral=["right",
        "oh",
        "okay",
        "alright"]

def audiototext(audio):  # audio file to text
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio = r.record(source)
        print("done recording")
    text = r.recognize_google(audio)
    
    return text

def recordtotext(audio):  # recording to text and audio file 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak ")
        audio = r.listen(source)
    text = r.recognize_google(audio)
    print("done recording")

    return text, audio

language = 'en'
def botspeak(line):
    myobj = gTTS(text = line, lang = language, slow = False)
    audio_file = "ques"+line[3:7]+".mp3"
    myobj.save(audio_file)

    # playing the converted file
    playsound(audio_file)
    os.remove(audio_file)