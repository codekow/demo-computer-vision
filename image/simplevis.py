import cv2
import utils
import os
display = utils.notebook_init()  # checks

cap = cv2.VideoCapture(0)

# Capture frame
ret, frame = cap.read()
if ret:
	cv2.imwrite('image.jpg', frame)

cap.release()
img = 'image.jpg'
