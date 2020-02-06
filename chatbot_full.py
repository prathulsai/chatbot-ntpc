from flask import Flask, render_template, request
import nltk
import numpy as np
import random
import pyodbc 
import string # to process standard python strings
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-JE511J3\SQLEXPRESS;'
                      'Database=test;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
f=open('chatbot.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()# converts to lowercase
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words
lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
def response(user_response):
    user_response=user_response.lower()
    if(user_response=='thanks' or user_response=='thank you' ):
        return "You are welcome.."
    if(greeting(user_response)!=None):
        return greeting(user_response)
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        cursor.execute("insert into dbo.unanswered(unanswered)values(?)",(user_response))
        cursor.commit()
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        cursor.execute("insert into dbo.Answered(answered)values(?)",(user_response))
        cursor.commit()
        return robo_response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(response(userText))


if __name__ == "__main__":
    app.run()