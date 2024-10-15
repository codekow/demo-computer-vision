#!/bin/bash
tkn pipeline start simplevis-build \
-w name=shared-workspace,\
volumeClaimTemplateFile=https://raw.githubusercontent.com/openshift/pipelines-tutorial/pipelines-1.8/01_pipeline/03_persistent_volume_claim.yaml \
-p deployment-name=simplevis-flyingthings \
-p git-url=https://github.com/redhat-na-ssa/simplevis.git \
-p git-revision=develop \
-p BUILD_EXTRA_ARGS='--build-arg TRAINING_NAME=flyingthings --build-arg TRAINING_VER=1.0 --build-arg WEIGHTS=flyingthings.pt --build-arg MODEL_CLASSES=flyingthings.yaml' \
-p IMAGE=image-registry.openshift-image-registry.svc:5000/simplevis/simplevis-flyingthings \
--use-param-defaults