# hadolint global ignore=DL3041
FROM registry.access.redhat.com/ubi9/python-39:1
# FROM quay.io/centos/centos:stream9

USER 0

WORKDIR /opt/app-root/src

COPY requirements.txt ./


VOLUME /opt/app/root/src

COPY . ./

USER 1001

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
