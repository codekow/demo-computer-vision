FROM ubi9/python-39:latest
USER root
RUN yum install -y libGL
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-9.noarch.rpm \
 && dnf -y install ffmpeg

RUN git clone --branch v6.2 https://github.com/ultralytics/yolov5.git
RUN mkdir uploaded-files
RUN mkdir detected-files
RUN wget -O yolov5/data/uavs2.yaml http://nexus.davenet.local:8081/repository/simplevis/model/uavs2.yaml
RUN wget -O yolov5/coco_uavs.pt http://nexus.davenet.local:8081/repository/simplevis/model/coco_uavs.pt
RUN wget -O yolov5/yolov5s.pt http://nexus.davenet.local:8081/repository/simplevis/model/yolov5s.pt

COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR yolov5 
RUN pip install -r requirements.txt 
EXPOSE 8000
WORKDIR /opt/app-root/src
#ENTRYPOINT ["/opt/app-root/bin/uvicorn","main:app","--host","0.0.0.0"]
