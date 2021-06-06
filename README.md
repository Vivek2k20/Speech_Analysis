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
#### 4.API can be accessed at "localhost:5000/api" using "POST" method and sending the data in JSON format.The Backend and logic is ready.
#### 5.API Testing UI can be access at "localhost:5000/api" using "GET" method.This was supposed to take inputs from the user and call the API and pass the inputs in form of JSON.But,we are stuck in the frontend.Unable to encode audio file into JSON and pass.So,The tool is unable to send the JSON Data. However,The Backend seems fine and should be able to handle JSON data it recieves.



## Tasks Done : 
#### 1.UI to upload files and transcribe
#### 2.Takes input in either audio wav file or from microphone.
#### 3.Question 1 is working with good accuracy.
#### 4.Question 2 is working with excellent accuracy.
#### 5.Question 3 is working with excellent accuracy.
#### 6.Unprocessed Transcribed Audio can also be obtained.
#### 7.API Endpoint created to handle requests

## Tasks Left :
#### 1.API Testing Tool(UI is done.Need to pass all form elements and audio in form of JSON to the API endpoint.)
