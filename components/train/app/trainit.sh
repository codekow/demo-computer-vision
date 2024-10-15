#!/bin/bash
# shellcheck disable=SC2164,SC2164,SC1107,SC2086

wget -O ${TRAINING_DATA}/dataset.tgz ${ARTI_REPO}/data/training/${DATASET_VER}/${DATASET} \
 && cd ${TRAINING_DATA} \
 && tar xzf dataset.tgz \
 && cp data.yaml ${YOLO_DIR}/data \
 && wget -O ${YOLO_DIR}/weights.pt ${ARTI_REPO}/model/${WEIGHTS}

# cd /opt/app-root/src
# python3.9 main.py

cd ${YOLO_DIR}

python3.9 train.py --data data.yaml \
--batch-size $BATCH_SIZE \
--weights weights.pt \
--project ${TRAINING_DATA} \
--img 640 \
--device 0 \
--epochs $EPOCHS

cd ${TRAINING_DATA}

tar czf artifacts.tgz exp

curl -v -u $ARTI_USER:$ARTI_PWD \
--upload-file ${TRAINING_DATA}/artifacts.tgz \
$ARTI_REPO/$TRAINING_NAME/$TRAINING_VER/artifacts.tgz

curl -v -u $ARTI_USER:$ARTI_PWD \
--upload-file ${TRAINING_DATA}/exp/weights/best.pt \
$ARTI_REPO/$TRAINING_NAME/$TRAINING_VER/$TRAINING_NAME.pt

curl -v -u $ARTI_USER:$ARTI_PWD \
--upload-file /usr/local/lib/python3.9/site-packages/yolov5/data/data.yaml \
$ARTI_REPO/$TRAINING_NAME/$TRAINING_VER/$MODEL_CLASSES

curl -v -u $ARTI_USER:$ARTI_PWD \
--upload-file ${TRAINING_DATA}/exp/results.csv \
$ARTI_REPO/$TRAINING_NAME/$TRAINING_VER/results.csv