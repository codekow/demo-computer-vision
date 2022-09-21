FROM quay.io/centos/centos:stream9

WORKDIR /opt/app-root/src
ARG YOLOv5_VERSION=6.2
ARG WEIGHTS=yolov5s

RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-9.noarch.rpm \
 && dnf -y install ffmpeg libGL git wget python3-pip \
 && dnf clean all

RUN mkdir -p /usr/local/lib/python3.9/site-packages \
 && cd /usr/local/lib/python3.9/site-packages \
 && git clone --branch v${YOLOv5_VERSION} --depth 1 https://github.com/ultralytics/yolov5.git \
 && pip install --no-cache-dir \
    -r /usr/local/lib/python3.9/site-packages/yolov5/requirements.txt

RUN cd /usr/local/lib/python3.9/site-packages/yolov5 \
 && wget -O data/uavs2.yaml https://s3.jharmison.com/simplevis/public/uavs2.yaml \
 && wget -O weights.pt https://s3.jharmison.com/simplevis/public/${WEIGHTS}.pt

COPY requirements.txt ./

ENV SIMPLEVIS_DATA=/opt/app-root/src/simplevis-data

RUN pip install --no-cache-dir -r requirements.txt \
 && mkdir -p ${SIMPLEVIS_DATA} \
 && chown 1001:1001 ${SIMPLEVIS_DATA}

COPY app/ ./

#USER 1001
USER 0
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/uvicorn"]
CMD ["main:app", "--host", "0.0.0.0"]
