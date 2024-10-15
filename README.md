# Computer Vision Demo

[![File Linting](https://github.com/redhat-na-ssa/simplevis/actions/workflows/linting.yaml/badge.svg)](https://github.com/redhat-na-ssa/simplevis/actions/workflows/linting.yaml)

This repo helps to demonstrate the use of computer vision, containers, and openshift

## Quickstart

Build model server via source

s2i strategy: `source`

```sh
APP_NAME=model-serving-cv

oc new-app \
  https://github.com/redhat-na-ssa/demo-computer-vision.git#peer-review \
  --name ${APP_NAME} \
  --strategy source \
  --context-dir /components/model

oc label all --all app=demo-computer-vision
```

Build model server via `Dockerfile`

s2i strategy: `docker`

```sh
APP_NAME=model-serving-cv-dockerfile
oc new-app \
  https://github.com/redhat-na-ssa/demo-computer-vision.git#peer-review \
  --label app=demo-computer-vision \
  --name ${APP_NAME} \
  --strategy docker \
  --context-dir /components/model
```

Expose API / model server - Route

```sh
oc expose service \
  ${APP_NAME} \
  --label app=demo-computer-vision \
  --port 8080 \
  --overrides='{"spec":{"tls":{"termination":"edge"}}}'
```

Build camera capture via `Dockerfile`

s2i strategy: `docker`

```sh
APP_NAME=camera-capture-cv
oc new-app \
  https://github.com/redhat-na-ssa/demo-computer-vision.git#peer-review \
  --label app=demo-computer-vision \
  --name ${APP_NAME} \
  --strategy docker \
  --context-dir /components/camera
```

Setup Liveness Probe

```sh
oc set probe deploy/${APP_NAME} \
  --liveness \
  --get-url=http://:8080/healthz
```

## TODO

- [ ] tell story
- [ ] address dependencies
