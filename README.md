# Speech Analysis.
#### Contains a web app and API.
#### Uses Flask.
#### Takes the following input : question id,options and audio.The answer is returned.

## Team Members : 
#### Niharika C
#### Phoebe P
#### Ramya B S 
#### Vivek M R


##  INFO/STEPS TO RUN :
#### 1.Create a virtual environment if necessary and install the requirements mentioned in requirements.txt
#### 2.Run app.py
#### 3.Web App is hosted at "localhost:5000".Works fine.
#### 4.API can be accessed at "localhost:5000/api" using "POST" method and sending the data in JSON format.
#### 5.API Testing UI can be access at "localhost:5000/api/test" using "GET" method.This was supposed to take inputs from the user and call the API and pass the inputs in form of JSON.There seems to be a problem in recieving the data as JSON in the API.



## Tasks Done : 
#### 1.UI to upload files and transcribe
#### 2.Takes input in either audio wav file or from microphone.
#### 3.Question 1 is working with good accuracy.
#### 4.Question 2 is working with excellent accuracy.
#### 5.Question 3 is working with excellent accuracy.
#### 6.Unprocessed Transcribed Audio can also be obtained.
#### 7.API Endpoint created to handle requests
#### 8.API Testing Tool is created.Sends JSON data to the API.

## Tasks Left :
#### 1.Discovered bugs in the API. Doesn't recieve JSON data correctly.Need to work on it.
