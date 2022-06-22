# FROM registry.access.redhat.com/ubi8/python-38:latest for raspberry pi
# FROM ubi8/python-38:latest
FROM model:latest

USER root
RUN yum install -y libGL
RUN pip3 install flask requests bs4 flask_restful waitress
RUN pip3 install opencv-python

WORKDIR /opt/app-root/src
COPY flask flask
ENV FLASK_APP=flask/main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV CAPTURE_PATH=/opt/app-root/src/flask/static
ENV YOLODIR=/opt/app-root/src/yolov5
ENV UPLOAD_FOLDER=/opt/app-root/src/flask/static/incoming
ENV MODEL_SERVER="http://localhost:5001"
ENV ENVIRONMENT_NAME="RHEL+Podman"

EXPOSE 5001
ENTRYPOINT ["/opt/app-root/src/flask/main.py"]
