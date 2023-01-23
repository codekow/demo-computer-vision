import os
from pathlib import Path
import shutil

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

def app_init():
    global APP_DATA
    APP_DATA = Path(os.environ.get("SIMPLEVIS_DATA", "data"))

    os.makedirs(APP_DATA.joinpath("upload"), exist_ok=True)
    os.makedirs(APP_DATA.joinpath("detect"), exist_ok=True)

    global SAFE_2_PROCESS
    global VIDEO_EXTS
    SAFE_2_PROCESS = [".JPG", ".JPEG", ".PNG", ".M4V", ".MOV", ".MP4"]
    VIDEO_EXTS = [".M4V", ".MOV", ".MP4"]

app_init()

def isSafe(filename):
    global SAFE_2_PROCESS
    SAFE_2_PROCESS = [".JPG", ".JPEG", ".PNG", ".M4V", ".MOV", ".MP4"]
    return Path(filename).suffix.upper() in SAFE_2_PROCESS

app = APIRouter(
    prefix="/detect",
)


# # Load the classes
# with open(YOLO_DIR.joinpath('data').joinpath('data.yaml'), 'r') as f:
#     try:
#         parsed_yaml = yaml.safe_load(f)
#         OBJECT_CLASSES = parsed_yaml['names']
#     except yaml.YAMLError as exc:
#         raise RuntimeError(f"Unable to load classes from yaml: {str(exc)}")
#     except Exception as exc:
#         raise RuntimeError(f"Unable to identify class names: {str(exc)}")


@app.post("/file")
def detect_uploaded_file(file: UploadFile):
    if not isSafe(file.filename):
        raise HTTPException(
            status_code=415,
            detail=(
                f"Cannot process that file type. " f"Supported types: {SAFE_2_PROCESS}"
            ),
        )

    try:
        contents = file.file.read()
        with open(APP_DATA.joinpath("upload", file.filename), "wb") as f:
            f.write(contents)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        file.file.close()

    return {
        "filename": file.filename,
        "contentType": file.content_type,
        "save_path": APP_DATA.joinpath("upload", file.filename),
    }


@app.post("/camera")
def detect_with_attached_camera():
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    webcam_filename = "webcam" + date_time + ".jpg"
    _ = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "v4l2",
            "-video_size",
            "640x480",
            "-i",
            "/dev/video0",
            "-frames:v",
            "1",
            str(UPLOAD_DIR.joinpath(webcam_filename)),
        ],
        stdout=subprocess.PIPE,
    )

    detect_args = {
        "weights": WEIGHTS_FILE,
        "source": str(UPLOAD_DIR.joinpath(webcam_filename)),
        "project": DETECT_DIR,
        "exist_ok": True,
    }
    detect_args["save_txt"] = True

    # Actually run the inference
    yolov5_detect(**detect_args)

    labels = get_labels(webcam_filename)
    return {
        "filename": webcam_filename,
        # "contentType": file.content_type,
        "detectedObj": labels,
        "save_path": UPLOAD_DIR.joinpath(webcam_filename),
        "data": {},
    }

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
        idx = 0
        for c in OBJECT_CLASSES:
            cname = OBJECT_CLASSES[idx]
            count = countX(det_list, idx)
            if count > 0:
                obj = {"object": cname, "count": count}
                obj_list.append(obj)
            idx += 1
        obs = obj_list
    except Exception as e:
        print("Exception: " + str(e))
        obs = ["no objects detected"]
    return obs
