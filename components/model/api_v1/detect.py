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
                f"Cannot process {file.filename}. " f"Supported types: {SAFE_2_PROCESS}"
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
    try:
        detect_camera()
    except Exception:
        raise HTTPException(status_code=503, detail="no camera attached")
    
    return "ok"
