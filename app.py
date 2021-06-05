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


def det_range(opl):
    a=[0,]
    #print(opl)
    for x in opl:
        a=a+[int(s) for s in x.split("-")]
    a=a+[100]
    return a




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
        #print(opl)
        #print(b)
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
    elif int(qid)==2:
        buffer=opl.copy()
        for i in range(len(opl)):
            opl[i]=opl[i].replace(">","")
            opl[i]=opl[i].replace("<","")
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
        while (b[0]>=a[i*2+1]) :
            i=i+1
        result.append(buffer[i])
    elif int(qid)==3:
        a=datefinder.find_dates(word)
        for dob in a:
            datestring=dob.strftime("%d/%m/%Y")
            result.append(datestring)
    elif int(qid)==4:
        result.append(word)
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
    #samplet="I earn 23 Lakh"
    #sampleo=["<5lakh","5lakh-15lakh","15lakh-20lakh","20lakh>"]
    #print(getresult("2",sampleo,samplet))
    questions=["Do you suffer from any health diseases?","What’s your annual income?","What is your dob?","No questions.Just return voice"]
    if request.method=="POST":
        qid=request.form['qid']
        options=request.form['options']
        if ((qid==1)or(qid==2))and(options==""):
            return render_template('index.html',transcript="The Questions chosen require to enter options",questions=questions)
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
        transcript=r.recognize_google(data,key=None)
        transcript=getresult(qid,opl,transcript)
        return render_template('index.html',transcript=transcript,questions=questions)
    return render_template('index.html',transcript=transcript,questions=questions)







if __name__=="__main__":
    app.run(debug=True,threaded=True)