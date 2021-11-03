import cv2 as cv
# Виводження фотки
# img = cv.imread('Photos/1.jpg')

# cv.imshow('name',img)

# cv.waitKey(0)




# 
# Виводження відео

capture = cv.VideoCapture(0)

while True:
	isTrue, frame = capture.read()
	cv.imshow('Video',frame)

	if cv.waitKey(20) & 0xFF==ord('d'):
		break

capture.release()
cv.destroyALLWindows()		

