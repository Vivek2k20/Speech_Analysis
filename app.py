from flask import Flask,render_template,request,redirect,jsonify
from textblob import TextBlob
import speech_recognition as sr
import pyaudio
import datefinder
from datetime import datetime



app = Flask(__name__)


''' 
API PART TO WORK ON LATER


Create some test data for our request in the form of a list of dictionaries.
questions = [
    {
        'question_key': "q1",
        'options':["Diabetes","Thyroid","Cancer"],
        'audio': base {} audio
    },
    {
        'question_key': "q2",
        'options':["<2lakh","2lakh-5lakh","5lakh-10lakh","10lakh>"],
        'audio': base {} audio
    },
    {
        'question_key': "q3",
        'options':[],
        'audio': base {} audio
    }
]


This is the URL FOr which Requests are handled by the API
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(questions)

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
        print(opl)
        print(b)
        for a in opl:
            if a in word:
                result.append(a)
                if(a in b):
                    b.remove(a)
            elif (("other" in opl)or("others" in opl)) and (a):
                if "other" in opl:
                    result.append("other")
                else:
                    result.append("others")
    elif int(qid)==3:
        a=datefinder.find_dates(word)
        for dob in a:
            datestring=dob.strftime("%d/%m/%Y")
            result.append(datestring)
        '''nwords=TextBlob(word)
        a=nwords.noun_phrases
        for x in a:
            x=x.lower()
        for i in opl:
            try:
                i=i.lower()
                ind=a.index(i)
                result.append(i)
            except:
                try:
                    ind=a.index("others")
                    result.append("others")
                except:
                    try:
                        ind=a.index("other")
                        result.append("other")
                    except:
                        continue
            elif qid==2:
                a=[0,]
            '''

    return result





@app.route("/",methods=["GET","POST"])
def index():
    transcript=""
    samplet="I was born on 25th of June 2000"
    sampleo=[]
    print(getresult("3",sampleo,samplet))
    questions=["Do you suffer from any health diseases?","What’s your annual income?","What is your dob?"]
    if request.method=="POST":
        qid=request.form['qid']
        options=request.form['options']
        opl=options.split (",")
        if "file" not in request.files:
            mic = sr.Microphone()
            print("Listening")
            with mic as source:
                r=sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                data = r.listen(source)
        print("File Recieved")
        file=request.files["file"]
        if file.filename=="":
            mic = sr.Microphone()
            print("Listening")
            with mic as source:
                r=sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                data = r.listen(source)
        if file:
            r=sr.Recognizer()
            audioFile=sr.AudioFile(file)
            with audioFile as source:
                r.adjust_for_ambient_noise(source,duration=0.5)
                data=r.record(source)
        transcript=r.recognize_google(data,key=None)
        if (int(qid)==1)or(int(qid)==3):
            transcript=getresult(qid,opl,transcript)
        else:
            transcript="Returning just the words since qid is 2.The code isn't ready yet for that.Voice words : "+transcript
        return render_template('index.html',transcript=transcript,questions=questions)
    return render_template('index.html',transcript=transcript,questions=questions)







if __name__=="__main__":
    app.run(debug=True,threaded=True)