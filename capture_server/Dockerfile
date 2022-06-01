# FROM registry.access.redhat.com/ubi8/python-38:latest for raspberry pi
FROM ubi8/python-38:latest
USER root
RUN yum install -y libGL
RUN pip3 install flask requests bs4 flask_restful waitress twine
RUN pip3 install opencv-python
COPY flask flask

ENV FLASK_APP=flask/main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV CAPTURE_PATH=/data/simplevis
# ENV NEXUS_USER=admin
# ENV NEXUS_PASS=admin123
# ENV NEXUS_URL=http://nexus-nexus.apps.ocpsno.davenet.local

EXPOSE 5000
# ENV LC_ALL=en_US.utf-8
# ENV LANG=en_US.utf-8
ENTRYPOINT ["/opt/app-root/src/flask/main.py"]
