FastAPI Simple Object Detection
===============================

To access:
----------

Open [docs](docs) in your browser to access the Swagger UI

To build:
---------

```sh
podman build . -t simplevis:pre-trained
podman build . --build-arg WEIGHTS=coco_uavs -t simplevis:uavs
```

podman build . --build-arg WEIGHTS=flyingthings.pt \
--build-arg TRAINING_NAME=flyingthings \
--build-arg MODEL_CLASSES=flyingthings.yaml \
--build-arg TRAINING_VER=1.0 \
-t nexus.davenet.local:8080/simplevis/simplevis:flyingthings

To run:
-------

With the pre-trained weights:

```sh
podman run -d --name simplevis -p 8080:8080 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:pretrained
```

With the custom weights:
```sh
podman run -d --name simplevis -p 8080:8080 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:uavs
```
