#!/usr/bin/env python3.8
from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from flask_restful import reqparse, abort, Api, Resource
from waitress import serve, logging
import requests
import os
import glob
from bs4 import BeautifulSoup
from html import unescape

from functions.capture_functions import *
from functions.model_functions import *

app = Flask(__name__,template_folder='templates',static_folder='static')
api = Api(app)

parser = reqparse.RequestParser()

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

filepath = os.getenv('CAPTURE_PATH')
yolodir = os.getenv('YOLODIR')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'jpg'}
model_server = os.getenv('MODEL_SERVER')
environment_name = os.getenv('ENVIRONMENT_NAME')

class Test(Resource):
    def get(self):
        x = test()
        return jsonify(x)

class Capture(Resource):
    def get(self):
        x = capture()
        return jsonify(x)

class Detect(Resource):
    def get(self):
        x = detect()
        return jsonify(x)

api.add_resource(Detect,'/model/detect')
api.add_resource(Test,'/model/test')
api.add_resource(Capture,'/model/capture')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.context_processor
def inject_user():
    infiles = glob.glob(filepath+"/incoming/*")
    dtfiles = reversed(glob.glob(filepath+"/detected/*"))
    captured = reversed(glob.glob(filepath+"/captured/*"))
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
    return dict(incoming=incoming_files, detected=detected_files, captured=captured_files, environment_name=environment_name)
@app.route('/')
def web_hello():
    return render_template('index.html')

@app.route('/demo1')
def web_demo1():
    return render_template('capture.html')

@app.route('/gallery')
def web_gallery():
    return render_template('gallery.html')

@app.route('/capture')
def web_capture():
    resp = requests.get(url=model_server+"/model/capture")
    return render_template('capture.html')

@app.route('/detect')
def web_detect():
    resp = requests.get(url=model_server+"/model/detect")
    return render_template('gallery.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def web_upload_file():
    # Delete any leftover uploads
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)

    isExist = os.path.exists(UPLOAD_FOLDER)
    if not isExist:
        os.mkdir(UPLOAD_FOLDER)
    
    if request.method == 'POST':
        f = request.files['file']
        f.save(UPLOAD_FOLDER+'/'+f.filename)
        return render_template('capture.html')

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5001)
