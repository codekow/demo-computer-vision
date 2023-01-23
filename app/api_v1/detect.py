from fastapi import APIRouter


def isSafe(filename):
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


# @app.post("/detect")
# def detect(file: UploadFile):
#     if not isSafe(file.filename):
#         raise HTTPException(
#             status_code=415,
#             detail=(
#                 f"Cannot process that file type. " f"Supported types: {SAFE_2_PROCESS}"
#             ),
#         )

#     my_ext = Path(file.filename).suffix.upper()
#     try:
#         contents = file.file.read()
#         with open(UPLOAD_DIR.joinpath(file.filename), "wb") as f:
#             f.write(contents)
#     except Exception as err:
#         raise HTTPException(status_code=500, detail=str(err))
#     finally:
#         file.file.close()

#     detect_args = {
#         "weights": WEIGHTS_FILE,
#         "source": UPLOAD_DIR.joinpath(file.filename),
#         "project": DETECT_DIR,
#         "exist_ok": True,
#     }
#     if my_ext not in VIDEO_EXTS:
#         detect_args["save_txt"] = True

#     # Actually run the inference
#     yolov5_detect(**detect_args)

#     if my_ext not in VIDEO_EXTS:
#         labels = get_labels(file.filename)
#         return {
#             "filename": file.filename,
#             "contentType": file.content_type,
#             "detectedObj": labels,
#             "save_path": UPLOAD_DIR.joinpath(file.filename),
#             "data": {},
#         }
#     else:
#         try:
#             # ffmpeg to transcode the video file
#             newext = os.path.splitext(file.filename)
#             newfile = newext[0] + ".mp4"
#             video_file = DETECT_DIR.joinpath("exp").joinpath(newfile)
#             temp_video_file = video_file.with_stem("temp")
#             video_file.rename(temp_video_file)
#             _ = subprocess.run(
#                 [
#                     "ffmpeg",
#                     "-i",
#                     str(temp_video_file),
#                     "-c:v",
#                     "libx264",
#                     "-preset",
#                     "slow",
#                     "-crf",
#                     "20",
#                     "-c:a",
#                     "aac",
#                     "-b:a",
#                     "160k",
#                     "-vf",
#                     "format=yuv420p",
#                     "-movflags",
#                     "+faststart",
#                     str(video_file),
#                 ],
#                 stdout=subprocess.PIPE,
#             )
#             os.remove(temp_video_file)
#             os.remove(UPLOAD_DIR.joinpath(file.filename))
#             video_file.rename(VIDEO_DIR.joinpath(newfile))
#         except Exception as err:
#             raise HTTPException(status_code=500, detail=str(err))
#         return {
#             "filename": file.filename,
#             "contentType": file.content_type,
#             "save_path": UPLOAD_DIR.joinpath(file.filename),
#             "data": {},
#         }


# @app.post("/detect/camera")
# def detect():
#     now = datetime.now()
#     date_time = now.strftime("%Y%m%d-%H%M%S")
#     webcam_filename = "webcam" + date_time + ".jpg"
#     _ = subprocess.run(
#         [
#             "ffmpeg",
#             "-y",
#             "-f",
#             "v4l2",
#             "-video_size",
#             "640x480",
#             "-i",
#             "/dev/video0",
#             "-frames:v",
#             "1",
#             str(UPLOAD_DIR.joinpath(webcam_filename)),
#         ],
#         stdout=subprocess.PIPE,
#     )

#     detect_args = {
#         "weights": WEIGHTS_FILE,
#         "source": str(UPLOAD_DIR.joinpath(webcam_filename)),
#         "project": DETECT_DIR,
#         "exist_ok": True,
#     }
#     detect_args["save_txt"] = True

#     # Actually run the inference
#     yolov5_detect(**detect_args)

#     labels = get_labels(webcam_filename)
#     return {
#         "filename": webcam_filename,
#         # "contentType": file.content_type,
#         "detectedObj": labels,
#         "save_path": UPLOAD_DIR.joinpath(webcam_filename),
#         "data": {},
#     }


# def countX(lst, x):
#     count = 0
#     for ele in lst:
#         if ele == x:
#             count = count + 1
#     return count


# def get_labels(filename):
#     label_dir = DETECT_DIR.joinpath("exp").joinpath("labels")
#     label_file = label_dir.joinpath(filename).with_suffix(".txt")
#     det_list = []
#     obs = []
#     try:
#         with open(label_file) as file:
#             lines = file.readlines()
#             lines = [line.rstrip() for line in lines]
#             for line in lines:
#                 thisline = line.split()
#                 det_list.append(int(thisline[0]))
#         det_list.sort()
#         obj_list = []
#         idx = 0
#         for c in OBJECT_CLASSES:
#             cname = OBJECT_CLASSES[idx]
#             count = countX(det_list, idx)
#             if count > 0:
#                 obj = {"object": cname, "count": count}
#                 obj_list.append(obj)
#             idx += 1
#         obs = obj_list
#     except Exception as e:
#         print("Exception: " + str(e))
#         obs = ["no objects detected"]
#     return obs
