# FastAPI For Yolov5 Detection

## API docs

Open [docs](docs) in your browser to access the Swagger UI

## For development

```
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## Build Container

```
podman build . -t simplevis:pre-trained
podman build . --build-arg WEIGHTS=coco_uavs -t simplevis:uavs
```

```
podman build . --build-arg WEIGHTS=flyingthings.pt \
--build-arg TRAINING_NAME=flyingthings \
--build-arg MODEL_CLASSES=flyingthings.yaml \
--build-arg TRAINING_VER=1.0 \
-t nexus.davenet.local:8080/simplevis/simplevis:flyingthings
```

## Run Container

With the pre-trained weights:

```
podman run -d --name simplevis -p 8080:8080 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:pretrained
```

With the custom weights:

```
podman run -d --name simplevis -p 8080:8080 -v simplevis-data:/opt/app-root/src/simplevis-data simplevis:uavs
```
