# uvicorn main:app --reload 
# uvicorn app:app --reload --host localhost --host 0.0.0.0 --port 9000

import subprocess
from fastapi import FastAPI, Path, UploadFile
from typing import Optional

app = FastAPI()

@app.get("/")
def index():
    return {"status": "Everything`s Groovy"}

@app.post("/pretrained")
def detect(file: UploadFile):
    try:
        contents = file.file.read()
        with open("uploaded-files/" + file.filename, 'wb') as f:
            f.write(contents)
    except Exception as err:
        return {"error": err}
    finally:
        file.file.close()
    
    result = subprocess.run(['python', 'detect.py','--weights','yolov5s.pt','--save-txt','--project',"detected-files",'--exist-ok','--source',"uploaded-files/" + file.filename], stdout=subprocess.PIPE)
    output = str(result.stdout)
    labels = get_labels(file.filename)

    return {"message": f"Successfully uploaded {file.filename}", "labels": labels}

@app.post("/detect")
def detect(file: UploadFile):
    try:
        contents = file.file.read()
        with open("uploaded-files/" + file.filename, 'wb') as f:
            f.write(contents)
    except Exception as err:
        return {"error": err}
    finally:
        file.file.close()
    
    # result = subprocess.run(['python', 'detect.py','--weights','yolov5s.pt','--save-txt','--source',"uploaded-files/" + file.filename], stdout=subprocess.PIPE)
    result = subprocess.run(['python', 'detect.py','--weights','coco_uavs.pt','--save-txt','--project',"detected-files",'--exist-ok','--source',"uploaded-files/" + file.filename], stdout=subprocess.PIPE)
    output = str(result.stdout)
    labels = get_labels(file.filename)

    return {"message": f"Successfully uploaded {file.filename}", "labels": labels}

def get_labels(filename):
    return { "filename": filename, "object": "someobject", "count": 0 }