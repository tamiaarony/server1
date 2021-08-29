from flask import Flask, jsonify, request
from flask.helpers import make_response
from flask_cors import cross_origin
from google.cloud import speech
import io
from google.cloud import speech
import speech_recognition as sr
import wave, math, contextlib


app = Flask(__name__)

 
def transcribe_streaming(audio):
  r = sr.Recognizer()
  text = r.recognize_google(audio)
  return(text)

@app.route('/Transcrire', methods=['POST'])
@cross_origin()  # מגשר בין הפייתון לריאקט
def upload_file():
    if request.method == 'POST':
      #get the url and convert to string
      audio=request.get_data(parse_form_data=True).decode("utf-8")
      print(type(audio)) 
      print(audio)
      return jsonify(transcribe_streaming(audio))
    else:
      return 'No file'


if __name__ == "__main__":
  count=0
  app.run(debug=True)  # בריענון של הדף נותן שינויים שלא יצטרכו לפתוח שוב
