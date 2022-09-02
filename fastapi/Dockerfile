FROM ubi9:latest

WORKDIR /opt/app-root/src

RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-9.noarch.rpm \
 && dnf -y install ffmpeg libGL git wget python3-pip \
 && dnf clean all

RUN git clone --branch v6.2 https://github.com/ultralytics/yolov5.git \
 && wget -O yolov5/data/uavs2.yaml http://nexus.davenet.local:8081/repository/simplevis/model/uavs2.yaml \
 && wget -O yolov5/coco_uavs.pt http://nexus.davenet.local:8081/repository/simplevis/model/coco_uavs.pt \
 && wget -O yolov5/yolov5s.pt http://nexus.davenet.local:8081/repository/simplevis/model/yolov5s.pt

COPY app/ ./

RUN pip install -r requirements.txt \
 && pip install -r yolov5/requirements.txt \
 && mkdir -p uploaded-files detected-files \
 && chown 1001:1001 uploaded-files detected-files

USER 1001
ENV SIMPLEVIS_DATA=/opt/app-root/src/simplevis-data
EXPOSE 8000
ENTRYPOINT "/usr/local/bin/uvicorn"
CMD ["main:app", "--host", "0.0.0.0"]
