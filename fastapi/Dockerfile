#FROM ubi9/python-39:latest
FROM ubi9:latest
USER root
RUN yum install -y libGL git wget python3 python3-pip
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-9.noarch.rpm \
 && dnf -y install ffmpeg

WORKDIR /opt/app-root/src
RUN git clone --branch v6.2 https://github.com/ultralytics/yolov5.git
RUN wget -O yolov5/data/uavs2.yaml http://nexus.davenet.local:8081/repository/simplevis/model/uavs2.yaml
RUN wget -O yolov5/coco_uavs.pt http://nexus.davenet.local:8081/repository/simplevis/model/coco_uavs.pt
RUN wget -O yolov5/yolov5s.pt http://nexus.davenet.local:8081/repository/simplevis/model/yolov5s.pt

COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /opt/app-root/src/yolov5
RUN pip install -r requirements.txt
ENV SIMPLEVIS_DATA=/opt/app-root/src/simplevis-data
EXPOSE 8000
WORKDIR /opt/app-root/src
ENTRYPOINT ["/usr/local/bin/uvicorn","main:app","--host","0.0.0.0"]
