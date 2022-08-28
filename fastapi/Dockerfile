FROM ubi8/python-39:latest
USER root
RUN yum install -y libGL
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
# USER root
# RUN yum install -y libGL
# RUN pip install psutil IPython
EXPOSE 8000
