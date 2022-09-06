# simple vision
Simple sample computer vision demo for edge devices. This sample application is built around the yolov5 pre-trained model for object detection in an image and/or video. 

FastAPI Simple Object Detection
===============================

To build:
---------

```
podman build . -t simplevis:pretrained
podman build . --build-arg WEIGHTS=coco_uavs -t simplevis:uavs
```

To run:
-------

With the pretrained weights:

```
podman run -d --name simplevis -p 8000:8000 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:pretrained
```

With the custom weights:
```
podman run -d --name simplevis -p 8000:8000 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:uavs
```


To access:
----------

Open on http://localhost:8000/docs in your browser to access the Swagger UI

