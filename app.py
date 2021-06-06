'''
#################################################################
Importing stuff and initializing
#################################################################
'''
from flask import Flask,render_template,request,redirect,jsonify
import json,requests
from textblob import TextBlob
import speech_recognition as sr
import pyaudio
import datefinder
from base64 import b64encode
from datetime import datetime

ENCODING = 'utf-8'

app = Flask(__name__)




'''
#################################################################
List of Questions
#################################################################
'''
questions=["Do you suffer from any health diseases?","What’s your annual income?","What is your dob?","No questions.Just return voice"]





'''
#################################################################
Used for Determining the range of salaries given in options in case 2
#################################################################
'''
def det_range(opl):
    a=[0,]
    #print(opl)
    for x in opl:
        a=a+[int(s) for s in x.split("-")]
    a=a+[100]
    return a




'''
#################################################################
Analysing the transcript and extracting the answer
#################################################################
'''
def getresult(qid,opl,word):
    result=[]
    for x in opl:
        opl[opl.index(x)]=x.lower()
    word=word.lower()
    if int(qid)==1:
        nwords=TextBlob(word)
        b=nwords.noun_phrases
        for x in b:
            x=x.lower()
        if("other" in opl):
            opl.remove("other")
            opl.append("other")
        if("others" in opl):
            opl.remove("others")
            opl.append("others")
        if("none" in opl):
            opl.remove("none")
            opl.append("none")
        #print(opl)
        #print(b)
        for a in opl:
            if a in word:
                result.append(a)
                if(a in b):
                    b.remove(a)
        if (len(a)!=0)and(("other" in opl)or("others" in opl)):
            if "other" in opl:
                result.append("Other")
            else:
                result.append("Others")
        if (len(result)==0)and("none" in opl):
            result.append("None")
    elif int(qid)==2:
        buffer=opl.copy()
        for i in range(len(opl)):
            opl[i]=opl[i].replace(">","")
            opl[i]=opl[i].replace("<","")
            opl[i]=opl[i].replace("lakhs per annum","")
            opl[i]=opl[i].replace("lakhs","")
            opl[i]=opl[i].replace("lacs","")
            opl[i]=opl[i].replace("lakh","")
            opl[i]=opl[i].replace("lac","")
            opl[i]=opl[i].replace("lpa","")
        a=det_range(opl)
        #print(word)
        b=[int(s) for s in word.split(" ") if s.isdigit()]
        i=0
        #print(b)
        if(len(b)==0):
            result.append("Sorry,Processing failed.Either there was no answer or didn't catch your voice.Please try again")
            return result
        while not((b[0]>=a[i*2])and(b[0]<a[i*2+1])) :
            i=i+1
        result.append(buffer[i])
    elif int(qid)==3:
        a=datefinder.find_dates(word)
        for dob in a:
            datestring=dob.strftime("%d/%m/%Y")
            result.append(datestring)
    elif int(qid)==4:
        result.append(word)
    else:
        result.append("Unknown Question ID")
    return result





'''
#################################################################
Home/UI for testing logic
#################################################################
'''
@app.route("/",methods=["GET","POST"])
def index():
    transcript=""
    #samplet="I earn 23 Lakh"
    #sampleo=["<5lakh","5lakh-15lakh","15lakh-20lakh","20lakh>"]
    #print(getresult("2",sampleo,samplet))
    if request.method=="POST":
        qid=request.form['qid']
        options=request.form['options']
        if ((qid==1)or(qid==2))and(options==""):
            return render_template('index.html',transcript="The Questions chosen require to enter options.Since no option is given,The result is []",questions=questions)
        opl=options.split (",")
        if "file" not in request.files:
            mic = sr.Microphone()
            print("Listening")
            with mic as source:
                r=sr.Recognizer()
                r.adjust_for_ambient_noise(source,duration=0.5)
                data = r.listen(source)
        print("File Recieved")
        file=request.files["file"]
        #print(file)
        if file.filename=="":
            mic = sr.Microphone()
            print("Listening")
            with mic as source:
                r=sr.Recognizer()
                r.adjust_for_ambient_noise(source,duration=0.5)
                data = r.listen(source)
        if file:
            r=sr.Recognizer()
            audioFile=sr.AudioFile(file)
            with audioFile as source:
                r.adjust_for_ambient_noise(source,duration=0.5)
                data=r.record(source)
        try:
            transcript=r.recognize_google(data,key=None)
            transcript=getresult(qid,opl,transcript)
        except:
            transcript="No Internet Connection.Please try again after connecting to the internet."
        return render_template('index.html',transcript=transcript,questions=questions)
    return render_template('index.html',transcript=transcript,questions=questions)






@app.route('/api/test', methods=['GET','POST'])
def ctoj():
    if request.method=='POST':
        qid=request.form["question_key"]
        options=request.form["options"]
        audiofile=request.files["audio"]
        audio=b64encode(audiofile.read())
        audiostring=audio.decode(ENCODING)
        data={
            "qid":qid,
            "options":options,
            "audio":audiostring
        }
        print("entered ctoj")
        requests.post('http://127.0.0.1:5000/api',json=data)
        return render_template('api.html',questions=questions,transcript="")
    else:
        return render_template('api.html',questions=questions,transcript="")




'''
#################################################################
This is the URL endpoint for the API
#################################################################
'''
@app.route('/api', methods=['POST'])
def api():
    if request.method=='POST':
        json_data=request.json()
        if json_data==None:
            json_data=request.data()
        print (json_data)
        response={}
        qid=json_data['question_key']
        qid=int(qid[len(qid)-1])
        options=json_data['options']
        if ((qid==1)or(qid==2))and(options==""):
            response['answers']=[]
            return jsonify(response)
        audio_file=json_data['audio']
        if audio_file.filename=="":
            return("No file Uploaded.")
        r=sr.Recognizer()
        audioFile=sr.AudioFile(audio_file)
        with audioFile as source:
            r.adjust_for_ambient_noise(source,duration=0.5)
            adata=r.record(source)
        transcript=r.recognize_google(adata,key=None)
        opl=options.split (",")
        response['answers']=getresult(qid,opl,transcript)
        return jsonify(response)







'''
#################################################################
Running App
#################################################################
'''
if __name__=="__main__":
    app.run(debug=True,threaded=True)