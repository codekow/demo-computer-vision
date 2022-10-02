FastAPI Simple Object Detection
===============================

To build:
---------

```sh
podman build . -t simplevis:pretrained
podman build . --build-arg WEIGHTS=coco_uavs -t simplevis:uavs
```

podman build . --build-arg WEIGHTS=flyingthings.pt \
--build-arg TRAINING_NAME=flyingthings \
--build-arg MODEL_CLASSES=flyingthings.yaml \
--build-arg TRAINING_VER=1.0 \
-t nexus.davenet.local:8080/simplevis/simevis:flyingthings

To run:
-------

With the pretrained weights:

```sh
podman run -d --name simplevis -p 8000:8000 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:pretrained
```

With the custom weights:
```sh
podman run -d --name simplevis -p 8000:8000 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:uavs
```


To access:
----------

Open on http://localhost:8000/docs in your browser to access the Swagger UI

