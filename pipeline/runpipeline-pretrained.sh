#!/bin/bash
tkn pipeline start simplevis-build \
-w name=shared-workspace,\
volumeClaimTemplateFile=https://raw.githubusercontent.com/openshift/pipelines-tutorial/pipelines-1.8/01_pipeline/03_persistent_volume_claim.yaml \
-p deployment-name=mqtt \
-p git-url=https://github.com/redhat-na-ssa/simplevis.git \
-p git-revision=develop \
-p IMAGE=image-registry.openshift-image-registry.svc:5000/simplevis/simplevis-pretrained \
--use-param-defaults