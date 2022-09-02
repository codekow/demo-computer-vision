# uvicorn main:app --reload
# uvicorn app:app --reload --host localhost --host 0.0.0.0 --port 9000

import subprocess
import yaml
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from yolov5.detect import run as yolov5_detect
import os
import shutil
from pathlib import Path

ROOT_DIR = Path(
    os.environ.get(
        'SIMPLEVIS_DATA',
        Path(__file__).parent.resolve()
    )
)
YOLO_DIR = Path(
    os.environ.get(
        'YOLOv5_DIR',
        Path('/usr/local/lib/python3.9/site-packages/yolov5')
    )
)

WEIGHTS_FILE = YOLO_DIR.joinpath('weights.pt')
UPLOAD_DIR = ROOT_DIR.joinpath("uploaded-files")
DETECT_DIR = ROOT_DIR.joinpath("detected-files")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DETECT_DIR, exist_ok=True)

SAFE_2_PROCESS = [".JPG", ".JPEG", ".PNG", ".M4V", ".MOV", ".MP4"]
VIDEO_EXTS = [".M4V", ".MOV", ".MP4"]


# Load the classes
with open(YOLO_DIR.joinpath('data').joinpath('uavs2.yaml'), 'r') as f:
    try:
        parsed_yaml = yaml.safe_load(f)
        OBJECT_CLASSES = parsed_yaml['names']
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Unable to load classes from yaml: {str(exc)}")
    except Exception as exc:
        raise RuntimeError(f"Unable to identify class names: {str(exc)}")

app = FastAPI()


@app.get("/")
def index():
    return {"status": "Everything`s Groovy"}


@app.get("/uploads/get")
def getUploadList():
    return {"images": [f.stem for f in UPLOAD_DIR.iterdir()]}


@app.get("/uploads/get/image/{fname}")
async def main(fname):
    return FileResponse(DETECT_DIR.joinpath("exp").joinpath(fname))


@app.get("/uploads/get/labels/{fname}")
def getLabels(fname):
    labels = get_labels(fname)
    return {"labels": labels}


@app.get("/cleanall")
def cleanall():
    try:
        for f in UPLOAD_DIR.iterdir():
            os.remove(f)
        exp_dir = DETECT_DIR.joinpath("exp")
        for detection in exp_dir.iter_dir():
            shutil.rmtree(detection)
        return {"message": "All directories cleaned."}
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"An error has occurred: {str(err)}"
        )


@app.post("/detect")
def detect(file: UploadFile):
    if not isSafe(file.filename):
        raise HTTPException(
            status_code=415,
            detail=(
                f"Cannot process that file type. "
                f"Supported types: {SAFE_2_PROCESS}"
            )
        )

    my_ext = Path(file.filename).suffix.upper()
    try:
        contents = file.file.read()
        with open(UPLOAD_DIR.joinpath(file.filename), 'wb') as f:
            f.write(contents)
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=str(err)
        )
    finally:
        file.file.close()

    detect_args = {
        'weights': WEIGHTS_FILE,
        'source': UPLOAD_DIR.joinpath(file.filename),
        'project': DETECT_DIR,
        'exist_ok': True,
    }
    if my_ext not in VIDEO_EXTS:
        detect_args['save_txt'] = True

    # Actually run the inference
    yolov5_detect(**detect_args)

    if my_ext not in VIDEO_EXTS:
        labels = get_labels(file.filename)
        return {
            "filename": file.filename,
            "contentType": file.content_type,
            "detectedObj": labels,
            "save_path": UPLOAD_DIR.joinpath(file.filename),
            "data": {}
        }
    else:
        try:
            # ffmpeg to transcode the video file
            video_file = DETECT_DIR.joinpath('exp').joinpath(file.filename)
            temp_video_file = video_file.with_stem('temp')
            video_file.rename(temp_video_file)
            _ = subprocess.run([
                'ffmpeg',
                '-i',
                str(temp_video_file),
                '-c:v',
                'libx264',
                '-preset',
                'slow',
                '-crf',
                '20',
                '-c:a',
                'aac',
                '-b:a',
                '160k',
                '-vf',
                'format=yuv420p',
                '-movflags',
                '+faststart',
                str(video_file)
            ], stdout=subprocess.PIPE)
            os.remove(temp_video_file)
        except Exception as err:
            raise HTTPException(
                status_code=500,
                detail=str(err)
            )
        return {
            "filename": file.filename,
            "contentType": file.content_type,
            "save_path": UPLOAD_DIR.joinpath(file.filename),
            "data": {}
        }


def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


def get_labels(filename):
    label_dir = DETECT_DIR.joinpath("exp").joinpath("labels")
    label_file = label_dir.joinpath(filename).with_suffix(".txt")
    det_list = []
    obs = []
    try:
        with open(label_file) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            for line in lines:
                thisline = line.split()
                det_list.append(int(thisline[0]))
        det_list.sort()
        obj_list = []
        for c in OBJECT_CLASSES:

            cname = OBJECT_CLASSES[c]
            count = countX(det_list, c)
            if count > 0:
                obj = {"object": cname, "count": count}
                obj_list.append(obj)
        obs = obj_list
    except Exception:
        obs = ["no objects detected"]
    return obs


def isSafe(filename):
    return Path(filename).suffix.upper() in SAFE_2_PROCESS
