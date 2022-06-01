# FROM registry.access.redhat.com/ubi8/python-38:latest for raspberry pi
FROM ubi8/python-38:latest

RUN pip3 install flask requests bs4 flask_restful waitress
RUN git clone https://github.com/ultralytics/yolov5
WORKDIR yolov5 
RUN pip install -r requirements.txt 
USER root
RUN yum install -y libGL
RUN pip install psutil IPython
