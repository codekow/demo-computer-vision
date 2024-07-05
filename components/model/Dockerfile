# hadolint global ignore=DL3041
FROM registry.access.redhat.com/ubi9/python-39:1

COPY . /opt/app-root/src

USER 0

RUN chown -R 1001:0 ./

USER 1001

WORKDIR /opt/app-root/src

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir \
      -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["/opt/app-root/bin/uvicorn"]
CMD ["app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
