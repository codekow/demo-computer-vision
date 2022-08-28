git clone --branch v6.2 https://github.com/ultralytics/yolov5.git
mkdir uploaded-files
mkdir detected-files
wget -O yolov5/data/uavs2.yaml http://nexus.davenet.local:8081/repository/simplevis/model/uavs2.yaml
wget -O yolov5/coco_uavs.pt http://nexus.davenet.local:8081/repository/simplevis/model/coco_uavs.pt
wget -O yolov5/yolov5s.pt http://nexus.davenet.local:8081/repository/simplevis/model/yolov5s.pt
