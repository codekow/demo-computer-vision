#!/bin/bash
tkn pipeline start simplevis-build \
-w name=shared-workspace,\
volumeClaimTemplateFile=https://raw.githubusercontent.com/openshift/pipelines-tutorial/pipelines-1.8/01_pipeline/03_persistent_volume_claim.yaml \
-p deployment-name=simplevis-pretrained \
-p git-url=https://github.com/redhat-na-ssa/simplevis.git \
-p git-revision=develop \
-p WEIGHTS=yolov5s.pt \
-p TRAINING_NAME=pretrained \
-p TRAINING_VER=1.0 \
-p MODEL_CLASSES=coco128.yaml \
-p IMAGE=image-registry.openshift-image-registry.svc:5000/simplevis/simplevis-pretrained \
--use-param-defaults