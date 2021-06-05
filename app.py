from flask import Flask,render_template,request,redirect,jsonify
import speech_recognition as sr
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






@app.route("/",methods=["GET","POST"])
def index():
    transcript=""
    if request.method=="POST":
        if "file" not in request.files:
            return redirect(request.url)
        print("File Recieved")
        file=request.files["file"]
        if file.filename=="":
            return redirect(request.url)
        if file:
            recognizer=sr.Recognizer()
            audioFile=sr.AudioFile(file)
            with audioFile as source:
                data=recognizer.record(source)
            transcript=recognizer.recognize_google(data,key=None)
    return render_template('index.html',transcript=transcript)







if __name__=="__main__":
    app.run(debug=True,threaded=True)