#!/usr/bin/env python3
from flask_restful import reqparse, abort, Api, Resource
from waitress import serve, logging
from flask import Flask, redirect, url_for, render_template, request, flash
import requests
import os
import glob


filepath = os.getenv('CAPTURE_PATH')
yolodir = os.getenv('YOLODIR')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'jpg'}
model_server = os.getenv('MODEL_SERVER')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app=Flask(__name__,template_folder='templates',static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.context_processor
def inject_user():
    infiles = glob.glob(filepath+"/incoming/*.jpg")
    dtfiles = glob.glob(filepath+"/detected/*.jpg")
    captured = glob.glob(filepath+"/captured/*.jpg")
    incoming_files = []
    detected_files = []
    captured_files = []
    for c in infiles:
        iname = os.path.basename(c)
        incoming_files.append(iname)
    for f in dtfiles:
        fname = os.path.basename(f)
        detected_files.append(fname)
    for d in captured:
        ename = os.path.basename(d)
        captured_files.append(ename)
    return dict(incoming=incoming_files, detected=detected_files, captured=captured_files)
@app.route('/')    
def hello():
    return render_template('index.html')

@app.route('/capture')
def capture():
    resp = requests.get(url=model_server+"/capture")
    return render_template('index.html')

@app.route('/detect')
def detect():
    resp = requests.get(url=model_server+"/detect")
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    isExist = os.path.exists(UPLOAD_FOLDER)
    if not isExist:
        os.mkdir(UPLOAD_FOLDER)
    
    if request.method == 'POST':
        f = request.files['file']
        f.save(UPLOAD_FOLDER+'/'+f.filename)
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)





# app = Flask(__name__)
# api = Api(app)

# parser = reqparse.RequestParser()

# logger = logging.getLogger('waitress')
# logger.setLevel(logging.INFO)

# class Test(Resource):
#     def get(self):
#         x = test()
#         return jsonify(x)

# class Capture(Resource):
#     def get(self):
#         x = capture()
#         return jsonify(x)

# class Detect(Resource):
#     def get(self):
#         x = detect()
#         return jsonify(x)

# api.add_resource(Detect,'/detect')
# api.add_resource(Test,'/test')
# api.add_resource(Capture,'/capture')

# if __name__ == "__main__":
#     serve(app, host='0.0.0.0', port=5000)
