# FROM ubi9:latest
# FROM quay.io/centos/centos:stream9
FROM docker.io/nvidia/cuda:11.7.0-runtime-ubi8
# FROM docker.io/nvidia/cuda:10.1-runtime-ubi8

WORKDIR /opt/app-root/src
ENV TRAINING_NAME=flyingthings
ENV TRAINING_VER=X.X
ENV DATASET_VER=1.0
ENV DATASET=dataset_flyingthings.tgz
ENV MODEL_CLASSES=flyingthings.yaml
ENV YOLOv5_VERSION=6.2
ENV PYDIR=/usr/local/lib/python3.9/site-packages
ENV YOLO_DIR=${PYDIR}/yolov5
ENV WEIGHTS=yolov5s.pt
ENV BATCH_SIZE=16
ENV EPOCHS=10
ENV ARTI_REPO=http://nexus.davenet.local:8081/repository/simplevis
ENV ARTI_USER=simplevis
ENV ARTI_PWD=simplevis123

RUN dnf install -y git wget libGL python39 \
 && pip-3.9 install --upgrade pip \
 && pip-3.9 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cu117 \
 && dnf clean all

RUN mkdir -p ${PYDIR} \
 && cd ${PYDIR} \
 && git clone --branch v${YOLOv5_VERSION} --depth 1 https://github.com/ultralytics/yolov5.git \
 && pip-3.9 install --no-cache-dir \
    -r ${YOLO_DIR}/requirements.txt

ENV TRAINING_DATA=${YOLO_DIR}/training

COPY requirements.txt /opt/app-root/src/

RUN cd /opt/app-root/src \
 && pip-3.9 install --no-cache-dir -r requirements.txt \
 && mkdir -p ${TRAINING_DATA} \
 && chown -R 1001:1001 ${TRAINING_DATA} 

COPY app/ /opt/app-root/src/

USER 1001
ENTRYPOINT ["/opt/app-root/src/trainit.sh"]