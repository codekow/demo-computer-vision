FastAPI Simple Object Detection
===============================

To build:
---------

```sh
podman build . -t simplevis:pretrained
podman build . --build-arg WEIGHTS=coco_uavs -t simplevis:uavs
```

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

