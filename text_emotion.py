from Empath import Empath
import re
import sys
from textblob import TextBlob
emo = Empath()
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

    