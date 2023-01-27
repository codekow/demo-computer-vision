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

app_init()

app = APIRouter(
    prefix="/file",
    responses={404: {"description": "Not found"}},
)

@app.get(
    "/all",
)
def get_all_uploaded_files():
    return {
        "files": [f.parts[-1] for f in APP_DATA.joinpath("upload").iterdir()],
    }

@app.get(
    "/all/delete",
    tags=["v1"],
)
def delete_all_uploaded_files():
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


@app.get(
    "/download/{fname}",
)
async def get_file_by_filename(fname: str):
    try:
        return FileResponse(path=str(APP_DATA.joinpath("upload").joinpath(fname)), filename=fname)
    except Exception as e:
        if "does not exist" in str(e):
            raise HTTPException(
                status_code=404,
                detail=f"No file named {fname} found"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Problem encountered while loading {fname}"
            )


@app.get(
    "/labels/{fname}",
    tags=["v1"],
)
def get_labels_by_filename(fname):
    labels = get_labels(fname)
    return {"labels": labels}
