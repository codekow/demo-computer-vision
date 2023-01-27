# hadolint global ignore=DL3041
FROM registry.access.redhat.com/ubi9/python-39:1

USER 0

WORKDIR /opt/app-root/src

USER 1001

COPY . ./

RUN pip install --no-cache-dir \
      -r requirements.txt && \
    chown -R 1001:0 ./

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
