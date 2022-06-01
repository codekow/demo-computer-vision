FROM ubi8/python-38:latest
RUN pip3 install flask requests bs4 flask_restful waitress
USER root
COPY flask flask
ENV FLASK_APP=flask/app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV CAPTURE_PATH=/opt/app-root/src/flask/static
ENV UPLOAD_FOLDER=/opt/app-root/src/flask/static/incoming
ENV MODEL_SERVER="http://localhost:5001"

EXPOSE 5005
ENTRYPOINT ["/opt/app-root/src/flask/app.py"]
