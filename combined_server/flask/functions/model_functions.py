import json
import os
import shutil
import requests
import glob
import subprocess
from timeit import default_timer as timer

time_taken = timer()
def test():
  jsondata = ['this is a test']
  return jsondata

def detect():
  filepath = os.getenv('CAPTURE_PATH')
  yolodir = os.getenv('YOLODIR')

  infiles = glob.glob(filepath+"/incoming/*")
   
  # Create directory if it's not there
  cdir = filepath+'/captured'
  if not os.path.exists(cdir):
    os.makedirs(cdir)

  detect_list = []
  for ifile in infiles:
    fname = os.path.basename(ifile)
    nFname = filepath+'/captured/'+fname
    os.rename(ifile, nFname)
    detect_list.append(nFname)

  # # Detect from uploaded images
  for cfile in detect_list:
    # print('python '+yolodir+'/detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source '+cfile)
    started = timer()
    dcommand = 'python '+yolodir+'/detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source '+cfile
    # os.wait()
    process = os.popen(dcommand)
    os.wait()
    ended = timer()
    time_taken = round(ended - started,2)

  # Gather all the processed files
  exfiles = glob.glob(yolodir+"/runs/detect/exp*/*")
  
  # Create directory if it's not there
  detdir = filepath+'/detected'
  if not os.path.exists(detdir):
    os.makedirs(detdir)
  
  # Upload detection results
  for xfile in exfiles:
    xfilename = os.path.basename(xfile)
    nXfile = detdir+'/'+xfilename
    shutil.copy(xfile, nXfile)

  # Delete detected files. TODO only delete when successful
  if os.path.exists(yolodir+"/runs/detect"):
    shutil.rmtree(yolodir+"/runs/detect")

  # ptime = ended - started 
  # processing_time = ptime.strftime("%H%M%S")
  return [{'incoming': infiles}, {'detect_list': detect_list}, {'processing_time': time_taken}]
