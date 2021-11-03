import cv2 
from flask import Flask,render_template,Response,request

app = Flask(__name__)


# additional


key_of_video_capture = 0


camera = cv2.VideoCapture(key_of_video_capture)


def generate_frames():
	while True:
		##read the camera frame
		success,frame = camera.read()

		if not success:
			break
		else:
			ret,buffer = cv2.imencode('.jpg',frame)
			frame = buffer.tobytes()	
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
	# if "open" in request.form:
	# 	key_of_video_capture = 0
	# if request.method == "GET":
	# 	key_of_video_capture = 0
	return render_template("index.html")

@app.route('/video')
def video():
	return Response(generate_frames(),mimetype = 'multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__" :
	app.run(debug = True)







# while True:
# 	isTrue, frame = capture.read()
# 	cv2.imshow('Video',frame)

# 	if cv2.waitKey(20) & 0xFF==ord('d'):
# 		break

# capture.release()
# cv2.destroyALLWindows()		




# Виводження фотки
# img = cv.imread('Photos/1.jpg')
# cv.imshow('name',img)
# cv.waitKey(0)
# Виводження відео