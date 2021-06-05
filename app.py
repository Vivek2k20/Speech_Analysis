from flask import Flask,render_template,request,redirect,jsonify
import speech_recognition as sr
import pyaudio
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
    print(qid,word)
    if int(qid)==1:
        for i in opl:
            ind=word.find(i)
            if ind!=-1:
                result.append(i)
    '''elif qid==2:
        a=[0,]
    '''

    return result





@app.route("/",methods=["GET","POST"])
def index():
    transcript=""
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
        if int(qid)==1:
            transcript=getresult(qid,opl,transcript)
        else:
            transcript="Returning just the words since quid is 2 or 3.These are not ready yet.Voice words : "+transcript
        return render_template('index.html',transcript=transcript,questions=questions)
    return render_template('index.html',transcript=transcript,questions=questions)







if __name__=="__main__":
    app.run(debug=True,threaded=True)