# FROM pn-50.davenet.local:8080/repository/simplevis/simplevis-model:1.0.6-aarch64 for raspberry pi
FROM model:latest

WORKDIR /opt/app-root/src
COPY flask flask
ENV FLASK_APP=flask/main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV CAPTURE_PATH=/data/simplevis
ENV NEXUS_USER=admin
ENV NEXUS_PASS=admin123
ENV NEXUS_URL=http://nexus-nexus.apps.ocpsno.davenet.local
ENV YOLODIR=/opt/app-root/src/yolov5

EXPOSE 5000
# ENV LC_ALL=en_US.utf-8
# ENV LANG=en_US.utf-8
ENTRYPOINT ["/opt/app-root/src/flask/main.py"]
