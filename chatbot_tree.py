from flask import Flask, render_template, request
import nltk
import numpy as np
import random
import time
import pyodbc 
import string
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-JE511J3\SQLEXPRESS;'
                      'Database=test;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
quick_dict={
    "1.1.1.1.0.0":"Login through e-services click on compliants tab choose 'reporting complaint' in hardware(pc & pereperial section)",
    "1.1.1.1.0.2":"""<a href="#">click here </a>to document""",
    "1.1.1.1.0.3":"please type your query we will revert back",
    "1.1.1.0.1":"""<a href="#">click here</a> to reset your password"""
    }
funct_dict={}
data1=open("data.txt","r").readlines()
data=[]
for i in data1:
    data.append(i.strip())
search_string="1.1.1"
level=3
inp=""
t_button=""" <button type="button">{}</button> """
t_link="""<a href="//www.ntpc.co.in" target="_blank">ntpc website</a>"""
t_outmsg="""<div class="outgoing_msg">
              <div class="sent_msg">
                <p>{}</p>
                </div>
            </div>"""
app = Flask(__name__)

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
def response(user_response):
    global level,search_string
    user_response=user_response.lower()
    if(user_response=='thanks' or user_response=='thank you' ):
        return "You are welcome.."
    if(greeting(user_response)!=None):
        return greeting(user_response)
    if(user_response=="link"):
        return t_link
    if(user_response=="back"):
        level-=1
        search_string=search_string[:-2]
        str1=""
        j=0
        for i in data:
            if(i.startswith(search_string) and i.count(".")==level):
                str1=str1+str(j)+"."+str(i.split(",")[1])+"<br/>"
                j=j+1
        return str1
    if(user_response=="menu"):
        str1=""
        j=0
        level=3
        search_string="1.1.1"
        for i in data:
            if(i.startswith(search_string) and i.count(".")==level):
                str1=str1+str(j)+"."+str(i.split(",")[1])+"<br/>"
                j=j+1
        return str1
    level+=1
    search_string+="."+user_response
    if search_string in quick_dict.keys():
        return quick_dict[search_string]
    str1=""
    j=0
    for i in data:
        if(i.startswith(search_string) and i.count(".")==level):
            str1=str1+str(j)+"."+str(i.split(",")[1])+"<br/>"
            j=j+1
    return str1
    

@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(response(userText))


if __name__ == "__main__":
    app.run(debug="true")