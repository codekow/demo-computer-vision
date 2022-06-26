import json
import os
import cv2
import shutil
from datetime import datetime

filepath = os.getenv('CAPTURE_PATH')

def test():
  jsondata = ['this is a test']
  return jsondata

def capture():

  now = datetime.now() # current date and time
  date_time = now.strftime("%Y%m%d-%H%M%S")

  # Delete any leftover uploads
  if os.path.exists(filepath+'/incoming'):
    shutil.rmtree(filepath+'/incoming')

  isExist = os.path.exists(filepath+'/incoming')
  if not isExist:
    os.mkdir(filepath+'/incoming')
  
  impath = filepath+'/incoming/image-'+date_time+'.jpg'
  cap = cv2.VideoCapture(0)

  # Capture frame
  ret, frame = cap.read()
  if ret:
    cv2.imwrite(impath, frame)
  cap.release()

  jsondata = {'captured': impath }
  return jsondata

def cleanall():
  if os.path.exists(filepath+'/incoming'):
    shutil.rmtree(filepath+'/incoming')
  if os.path.exists(filepath+'/captured'):
    shutil.rmtree(filepath+'/captured')
  if os.path.exists(filepath+'/detected'):
    shutil.rmtree(filepath+'/detected')

  jsondata = {'status': 'cleaned'}