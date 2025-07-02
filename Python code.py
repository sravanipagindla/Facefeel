#Python Code for Facefeel

from flask import Flask, render_template, Response, jsonify
import cv2
from deepface import DeepFace
import pyttsx3

app = Flask(__name__)

camera = cv2.VideoCapture(0)
prev_emotion = ""
current_quote = ""

quotes = {
'happy': "Keep smiling, it makes life beautiful.",
'sad': "Every day is a new beginning.",
'angry': "Stay calm, everything will be fine.",
'surprise': "Expect the unexpected!",
'neutral': "Stay positive and focused.",
'fear': "Face your fears with courage.",
'disgust': "See the beauty in everything."
}

engine = pyttsx3.init()

def gen_frames():
global prev_emotion, current_quote
while True:
success, frame = camera.read()
if not success:
break
else:
try:
result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
emotion = result[0]['dominant_emotion']

if emotion != prev_emotion:
prev_emotion = emotion
current_quote = quotes.get(emotion, "Stay strong and confident.")
engine.say(current_quote)
engine.runAndWait()

cv2.putText(frame, f'Emotion: {emotion}', (20, 30),
cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
except:
pass

ret, buffer = cv2.imencode('.jpg', frame)
frame = buffer.tobytes()
yield (b'--frame\r\n'
b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
return render_template('index.html')

@app.route('/video')
def video():
return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_quote')
def get_quote():
return current_quote

if __name__ == "__main__":
app.run(debug=True)
