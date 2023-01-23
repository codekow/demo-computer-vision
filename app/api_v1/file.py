import os
from pathlib import Path
import shutil

# import subprocess
# import yaml
# from datetime import datetime
# from yolov5.detect import run as yolov5_detect

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

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

app = APIRouter(
    prefix="/file",
    responses={404: {"description": "Not found"}},
)

@app.get(
    "/get",
)
def get_upload_list():
    return {
        "files": [f.parts[-1] for f in APP_DATA.joinpath("upload").iterdir()],
    }

@app.get(
    "/get/{fname}",
    tags=["v1"],
)
async def get_uploaded_info_by_filename(fname):
    try:
        file_ext = Path(fname).suffix.upper()
        if file_ext not in VIDEO_EXTS:
            return FileResponse(DETECT_DIR.joinpath("exp").joinpath(fname))
        else:
            return FileResponse(VIDEO_DIR.joinpath(fname))
    except RuntimeError as exc:
        if "does not exist" in str(exc):
            raise HTTPException(status_code=404, detail=f"No file named {fname} found")
        else:
            raise HTTPException(
                status_code=500, detail=f"Problem encountered while loading {fname}"
            )


@app.get(
    "/get/labels/{fname}",
    tags=["v1"],
)
def get_labels_by_filename(fname):
    labels = get_labels(fname)
    return {"labels": labels}


@app.get(
    "/cleanall",
    tags=["v1"],
)
def clean_all():
    UPLOAD_DIR = APP_DATA.joinpath("upload")
    try:
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
            app_init()
        return {"message": "upload directory clean"}
    except Exception as err:
        raise HTTPException(
            status_code=500, detail=f"An error has occurred: {str(err)}"
        )


