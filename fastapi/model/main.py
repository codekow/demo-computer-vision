# uvicorn main:app --reload 
# uvicorn app:app --reload --host localhost --host 0.0.0.0 --port 9000

import subprocess
import yaml
from fastapi import FastAPI, Path, UploadFile
from typing import Optional
from yaml import load, dump
import os

UPLOAD_DIR = "uploaded-files"
DETECT_DIR = "detected-files"
PRE_TRAINED = "yolov5s.pt"
CST_TRAINED = "coco_uavs.pt"
PRE_CLASSES = "coco128.yaml"
CST_CLASSES = "uavs2.yaml"
OBJECT_CLASSES = {}

# Load the classes
with open("data/" + CST_CLASSES, 'r') as stream:
    try:
        parsed_yaml=yaml.safe_load(stream)
        OBJECT_CLASSES = parsed_yaml['names']
    except yaml.YAMLError as exc:
        print(exc)    

app = FastAPI()

@app.get("/")
def index():
    return {"status": "Everything`s Groovy"}

@app.post("/pretrained")
def detect(file: UploadFile):
    try:
        contents = file.file.read()
        with open(UPLOAD_DIR + "/" + file.filename, 'wb') as f:
            f.write(contents)
    except Exception as err:
        return {"error": err}
    finally:
        file.file.close()
    
    result = subprocess.run(['python', 'detect.py','--weights',PRE_TRAINED,'--save-txt','--project',DETECT_DIR,'--exist-ok','--source',UPLOAD_DIR + "/" + file.filename], stdout=subprocess.PIPE)
    output = str(result.stdout)
    labels = get_labels(file.filename)

    return {"message": f"Successfully uploaded {file.filename}", "labels": labels}

@app.post("/detect")
def detect(file: UploadFile):
    try:
        contents = file.file.read()
        with open(UPLOAD_DIR + "/" + file.filename, 'wb') as f:
            f.write(contents)
    except Exception as err:
        return {"error": err}
    finally:
        file.file.close()
    
    result = subprocess.run(['python', 'detect.py','--weights',CST_TRAINED,'--save-txt','--project',DETECT_DIR,'--exist-ok','--source',UPLOAD_DIR + "/" + file.filename], stdout=subprocess.PIPE)
    output = str(result.stdout)
    labels = get_labels(file.filename)

    return {"message": f"Successfully uploaded {file.filename}", "labels": labels}

def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count

def get_labels(filename):
    label_file = os.path.splitext(DETECT_DIR + "/exp/labels/" + filename)[0] + ".txt"
    det_list = []
    with open(label_file) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for line in lines:
            thisline = line.split()
            det_list.append(int(thisline[0]))
            # print(OBJECT_CLASSES[int(thisline[0])])
            # print (thisline[0])
    det_list.sort()
    obj_list = []
    for c in OBJECT_CLASSES:
        cname = OBJECT_CLASSES[c]
        count = countX(det_list,c)
        if count > 0:
            obj = {"object": cname, "count": count}
            obj_list.append(obj)
    print(obj_list)
    return { "filename": filename, "objects": obj_list }