# hadolint global ignore=DL3041
# FROM registry.access.redhat.com/ubi9/python-39:1
FROM quay.io/centos/centos:stream9

USER 0

RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
                   https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-9.noarch.rpm \
                   http://mirror.stream.centos.org/9-stream/CRB/x86_64/os/Packages/ladspa-1.13-28.el9.x86_64.rpm \
                   https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-9.noarch.rpm && \
    /usr/bin/crb enable && \
    dnf -y install git wget python3-pip ffmpeg libGL && \
    dnf clean all

WORKDIR /opt/app-root/src

COPY requirements.txt ./

RUN pip install --no-cache-dir \
      -r requirements.txt && \
    mkdir -p ${SIMPLEVIS_DATA} && \
    chown -R 1001:0 ${SIMPLEVIS_DATA}

VOLUME /data

USER 1001

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
