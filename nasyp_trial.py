import cv2 
from flask import Flask,render_template,Response,request
import mediapipe as mp
import time
# additional
from gevent.pywsgi import WSGIServer


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

app = Flask(__name__)
camera = cv2.VideoCapture(0)

getVideo = False
buttonText = "Allow getting video"

def generate_frames():
	# while True:
	# 	##read the camera frame
	# 	success,frame = camera.read()

	# 	if not success:
	# 		break
	# 	else:
	# 		ret,buffer = cv2.imencode('.jpg',frame)
	# 		frame = buffer.tobytes()	
	# 	yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	with mp_hands.Hands(
	    min_detection_confidence=0.5,
	    min_tracking_confidence=0.5) as hands:
	    while camera.isOpened():

	        success, image = camera.read()

	        start = time.time()
	   
	        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

	        image.flags.writeable = False

	        
	        results = hands.process(image)

	        image.flags.writeable = True

	       
	        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	        if results.multi_hand_landmarks:
	          for hand_landmarks in results.multi_hand_landmarks:

	            mp_drawing.draw_landmarks(
	                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)



	        end = time.time()
	        totalTime = end - start

	        fps = 1 / totalTime
	        print("FPS: ", fps)

	        cv2.putText(image, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

	        cv2.imshow('MediaPipe Hands', image)



	        if cv2.waitKey(5) & 0xFF == 27:
	            break
	        if not success:
	        	break
	        else:
	        	ret,buffer = cv2.imencode('.jpg',image)
	        	image = buffer.tobytes()	
	        yield(b'--image\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
	camera.release()

@app.route('/')
def index():
	# if "open" in request.form:
	# 	key_of_video_capture = 0
	# if request.method == "GET":
	# 	key_of_video_capture = 0
	return render_template("index.html", getVideo = getVideo, buttonText = buttonText)

@app.route('/video')
def video():
	return Response(generate_frames(),mimetype = 'multipart/x-mixed-replace; boundary=image')


@app.route('/GetVideo', methods = ['GET', 'POST'])
def GetVideo():
	global getVideo, buttonText
	getVideo = not getVideo
	buttonText = "Dismiss getting video"
	if not getVideo:
		buttonText = "Allow getting video"
	return render_template("index.html", getVideo = getVideo, buttonText = buttonText)

if __name__ == "__main__" :
	  app.run(debug = True)
	# http_server = WSGIServer(('127.0.0.1', 5000), app)
	# http_server.serve_forever()
	 # WSGIServer(('127.0.0.1', 5000), app).serve_forever()