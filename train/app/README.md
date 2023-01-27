IMAGE_BASE = /data/simplevis-data/training/images
LABEL_BASE = /data/simplevis-data/training/labels
TRAIN_BASE = /data/simplevis-data/training/train_data

podman run -it \
 --rm -v simplevis-training:/usr/local/lib/python3.9/site-packages/yolov5/training \
 --user 0 \
 simplevis-train \
 /bin/bash

 podman run -it \
 --rm --entrypoint /bin/bash simplevis-train

 python3 train.py --data $MODEL_CLASSES --batch-size 16 --weights yolov5s.pt --img 640 --epochs $EPOCHS --project $TRAINING_DATA

 sudo podman run -e NVIDIA_VISIBLE_DEVICES=all nvidia/cuda:11.7.0-runtime-ubi8 nvidia-smi

 python3 train.py --data $MODEL_CLASSES --batch-size 2 --weights yolov5s.pt --img 640 --device 0 --epochs $EPOCHS --project $TRAINING_DATA

import torch
print(torch.cuda.is_available())

pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cu117

python train.py --data $MODEL_CLASSES --batch-size 32 --weights yolov5s.pt --img 640 --device 0 --epochs 100 --project $TRAINING_DATA

python train.py --data coco_uavs.yml --batch-size 32 --weights yolov5s.pt --img 640 --device 0 --epochs 60 --project training


python3.9 train.py --data flyingthings.pt \
--batch-size -1 \
--weights weights.pt \
--project ${TRAINING_DATA} \
--img 640 \
--device 0 \
--epochs 200


podman run -it --rm --user 0 -e "TRAINING_VER=2.1" -e "BATCH_SIZE=-1" --shm-size 2gb simplevis-train

curl -v -u simplevis:simplevis123 \
--upload-file dataset_flyingthings.tgz \
http://nexus.davenet.local:8081/repository/simplevis/data/training/1.0/dataset_flyingthings.tgz

curl -v -u simplevis:simplevis123 \
--upload-file flyingthings.yaml \
http://nexus.davenet.local:8081/repository/simplevis/model/flyingthings.yaml


podman run -it --rm --user 0 -e "TRAINING_VER=2.1" \
-e "BATCH_SIZE=-1" \
-e "EPOCHS=10" \
--shm-size 4gb \
simplevis-train

podman run -it --rm --user 0 -e "TRAINING_VER=1.0" \
-e "BATCH_SIZE=32" \
-e "EPOCHS=100" \
--shm-size 2gb \
simplevis-train
