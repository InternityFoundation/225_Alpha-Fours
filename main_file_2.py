from Empath import Empath
import re
import sys
from textblob import TextBlob
emo = Empath()
mysp = __import__("my-voice-analysis")

def sentiment(text):
    analysis = TextBlob(text)
    sent = analysis.sentiment
    return sent

def emotion(text):
    data = text
    data = data.replace("\n"," ").strip().lower().replace(".","")
    def clean(text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", text).split())

    data = clean(data)
    d = emo.analyze(data)

    dff={}
    for i in d:
        if(i in ['cheerfullness','pride','celebration','heroic','optimism','violence','hate','emotional','anger','disappointment']):
            dff[i]=d[i]
    return dff      

def voice_gender(audio_file, audio_path):
    return mysp.myspgender(audio_file, audio_path)
def voice_pronunciation(audio_file, audio_path):
    return mysp.mysppron(audio_file, audio_path)

def voice_syllables(audio_file, audio_path):
    return mysp.myspsyl(audio_file, audio_path)

def voice_pauses(audio_file, audio_path):
    return mysp.mysppaus(audio_file, audio_path)

def voice_rateOfSpeech(audio_file, audio_path):
    return mysp.myspsr(audio_file, audio_path)

def voice_articulationSpeed(audio_file, audio_path):
    return mysp.myspatc(audio_file, audio_path)

def voice_speakingTime(audio_file, audio_path):
    return mysp.myspst(audio_file, audio_path)

# ratio of the speaking duration to the total speaking duration
def voice_ratio(audio_file, audio_path):
    return mysp.myspbala(audio_file, audio_path)

# returns a pandas dataframe object containing all the parameters and their values
def voice_reportOverall(audio_file, audio_path): 
    return mysp.mysptotal(audio_file, audio_path)
