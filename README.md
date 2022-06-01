# simple vision
Simple sample computer vision demo for edge devices. This sample application is built around the yolov5 pre-trained model for object detection in a image and/or video. 

## Release 1.2
- Consolidated code
- Updated README file

## Release 1.1.2.1
- Changed ports for apps
- Updated instructions to deploy in a pod
- Changed default connection for webserver to pod

## Release 1.1.2
- Updated model dockerfile
- Updated combined server dockerfile
- Updated readme
- Create incoming if not exist
- OCP deployment
- Added upload creation when directory not found

## Release 1.1.0
- Updated README.md
- Added upload alternative for image capture

## Release 1.0.9
- Added simple webserver for model operation

## Release 1.0.8
- Added combined container with capture and detect.

## Release 1.0.7
- Removed output to Nexus
- Added write to staged folders on mount point
- Remove incoming and exp files when processed

## Release 1.0.6
- Added container build scripts

## Release 1.0.5 
- Uploads model detection output to Nexus
- Reorganized Dockerfiles for capture and model containers

## Release 1.0.3
- Runs multiple input files

## TODO
- Organize README.md file
- Create deployment for model container for OpenShift

## Building the containers
The containers used depends on the type of deployment and the location/configuration of any cameras. If the target environment is a single node with camera attached directly running podman, follow the instructions for `combined server`. If the camera is connected to a different device than the server running the model, follow the instructions for `multi server`

### Multi Server
Currently under development. 

### Combined Server
The combined server assumes a single node running podman with an attached camera. There are three containers that must be built:
- `model` - Contains the model code and components used to run yolov5 inference. Used only to build the main model serving container and speedup development on the serving code.
- `simplevis-full` - Built on the model container, it runs the model and serves it through a flask application. The API handles calls for capture and detection.
- `simplevis-web` - Contains a flask web application to interact with the model. 


Building the containers:
1. From the ``model_server/model`` directory, do a podman build.  Be sure to label `latest` as it is needed to build the simplevis-full container
```
podman build -t model:latest .
```

2. From the ``combined_server`` directory, do a podman build.
```
podman build -t simplevis-full .
```

3. From the ``web_server`` directory, do a podman build.
```
podman build -t simplevis-web .
```

## Running the capture container in podman
To enable access to an attached camera, the container must be launched with the "device" argument. ex: "`--device /dev/video0`".

The podman deployment will create a pod and two volumes for persistance and sharing between the servers. You can replace the volumes with paths on your node if you like.

Create the pod
```
podman pod create -n simplevis -p 5001:5001 -p 5005:5005 --device /dev/video0
```

Deploy the model serving container to the pod
```
podman run -d \
--name simplevis-full \
-v simplevis:/data/simplevis \
--pod simplevis \
simplevis-full
```

Deploy the web app container to the pod
```
podman run -d \
--name simplevis-web \
-v simplevis:/opt/app-root/src/flask/static \
--pod simplevis \
simplevis-web
```

## Accessing the application
Once the pod and containers are launched access the application via browser at:
```
http://<yournode>:5005/
```
The `capture` button will take a frame from the attached camera and post it to the model server. It should be visible in the `incoming` part of the web page. You can also click the `upload` button to select an image to upload to the `incoming` section.

Once you have added at least one image, click the `detect` button to start the object detection process. When complete you should see the original image under `captured` and the detected image under `detected`


When developing locally set the following environment variables before launching the flask app.
```
export FLASK_APP=flask/main.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export CAPTURE_PATH=<where your capture files will be created>
export NEXUS_USER=<username>
export NEXUS_PASS=<user password>
export NEXUS_URL=<base url for nexus>
export YOLODIR=<directory where yolov5 is cloned>
```
```
python flask/main.py
```
