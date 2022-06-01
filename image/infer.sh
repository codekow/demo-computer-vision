python simplevis.py
python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source $PWD/image.jpg
curl -v -u admin:admin123 --upload-file $PWD/image.jpg http://nexus-service-nexus.apps.ocp4.davenet.local/repository/simplevis-artifacts/1.0/image_raw.jpg
curl -v -u admin:admin123 --upload-file $PWD/runs/detect/exp/image.jpg http://nexus-service-nexus.apps.ocp4.davenet.local/repository/simplevis-artifacts/1.0/image_det.jpg
