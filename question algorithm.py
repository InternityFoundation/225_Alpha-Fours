Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> questions=[["Hi, thanks for coming in today.Think of me as a friend I do not judge people , I can not because  I am a computer.I will ask a few questions to get us started and please feel free to tell me anything , your answers are totally confidential.   So , how are you doing today? : "],
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
          "umm...I didn't get you . Can you please elaborate"]

positive=["that is great",
         "awesome",
         "that is good",
         "nice",
         "yeah",
         "cool"]
         
neutral=["hmm",
        "right",
        "oh",
        "okay",
        "alright"]



from textblob import TextBlob
def polarity(answer):
  return TextBlob(answer).polarity

def subjectivity(answer):
  return TextBlob(answer).subjectivity


polarity("i am sad")



weights=[2,0,2,2,3,4,3,4,4,5]
total_score=[a*b for a,b in zip(polarity_score,weights)]
print(total_score)


!pip install nltk


from textblob.classifiers import NaiveBayesClassifier
train = [
    ('I am depressed.', 'neg'),
    ('I want to kill myself', 'neg'),
    ('I feel very good about the place i live in.', 'pos'),
    ('I feel great today', 'pos'),
    ("I feel depressed most of the times ", 'neg'),
    ('I am very close to my family and friends', 'pos'),
    ('I am tired of this stuff.', 'neg'),
    ("a couple days ago my nephew didn't call me back , I was kinda mad 'cause i had set aside some time to spend with him and he just blew it off and didn't call me back. ", 'neg'),
    ('He is my sworn enemy!', 'neg'),
    ('My boss is horrible.', 'neg')
]
test = [
    ('This is depressing', 'neg'),
    ('I will kill myself', 'neg'),
    ("The place I live in is amazing", 'pos'),
    ("I am depressed", 'neg'),
    ('Gary is a friend of mine.', 'pos'),
    ("I can't believe I'm doing this.", 'neg')
]
