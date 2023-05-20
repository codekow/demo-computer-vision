import random
import os
import shutil
from pathlib import Path
from yolov5.train import run as yolov5_train


TRAINING_DATA = Path(
    os.environ.get(
        'TRAINING_DATA',
        Path(__file__).parent.resolve()
    )
)

IMAGE_BASE = TRAINING_DATA.joinpath("images")
LABEL_BASE = TRAINING_DATA.joinpath("labels")
TRAIN_BASE = TRAINING_DATA.joinpath("train_data")
VAL_IMAGE_DIR = TRAIN_BASE.joinpath("images/val")
TRAIN_IMAGE_DIR = TRAIN_BASE.joinpath("images/train")
TEST_IMAGE_DIR = TRAIN_BASE.joinpath("images/test")
VAL_LABEL_DIR = TRAIN_BASE.joinpath("labels/val")
TRAIN_LABEL_DIR = TRAIN_BASE.joinpath("labels/train")
TEST_LABEL_DIR = TRAIN_BASE.joinpath("labels/test")

YOLO_DIR = Path(
    os.environ.get(
        'YOLOv5_DIR',
        Path('/usr/local/lib/python3.9/site-packages/yolov5')
    )
)
WEIGHTS_FILE = YOLO_DIR.joinpath('weights.pt')
MODEL_FILE = os.environ.get('MODEL_CLASSES')
BATCH_SIZE = os.environ.get('BATCH_SIZE')
EPOCHS = os.environ.get('EPOCHS')

count = 0
# Iterate directory
for path in os.listdir(LABEL_BASE):
    # check if current path is a file
    if os.path.isfile(os.path.join(LABEL_BASE, path)):
        count += 1
num_test = round(count * .1)
num_val = round(count * .1)
num_train = count - (num_test + num_val)
print(str(count) + " total files in training set.")
print(str(num_test) + " will be user for test.")
print(str(num_val) + " will be used for val.")
print(str(num_train) + " remain for training.")

all_labels = []
for i in LABEL_BASE.iterdir():
    all_labels.append(i)

val_test_list = random.choices(all_labels, k=num_val+num_test)

for x in range(0,num_val):
    ifile = os.path.basename(val_test_list[x])
    my_ext = os.path.splitext(ifile)[0]
    shutil.copy(all_labels[x], VAL_LABEL_DIR.joinpath(ifile)) #Label
    shutil.copy(IMAGE_BASE.joinpath(my_ext + ".jpg"), VAL_IMAGE_DIR.joinpath(my_ext + ".jpg")) #Image

    shutil.copy(all_labels[x], TRAIN_LABEL_DIR.joinpath(ifile)) #Label
    shutil.copy(IMAGE_BASE.joinpath(my_ext + ".jpg"), TRAIN_IMAGE_DIR.joinpath(my_ext + ".jpg")) #Image

    # print("val: " + str(x) + ": " + my_ext)
for x in range(num_val,num_test + num_val):
    ifile = os.path.basename(val_test_list[x])
    my_ext = os.path.splitext(ifile)[0]
    shutil.copy(all_labels[x], TEST_LABEL_DIR.joinpath(ifile)) #Label
    shutil.copy(IMAGE_BASE.joinpath(my_ext + ".jpg"), TEST_IMAGE_DIR.joinpath(my_ext + ".jpg")) #Image

    shutil.copy(all_labels[x], TRAIN_LABEL_DIR.joinpath(ifile)) #Label
    shutil.copy(IMAGE_BASE.joinpath(my_ext + ".jpg"), TRAIN_IMAGE_DIR.joinpath(my_ext + ".jpg")) #Image    
    # print("test: " + str(x) + ": " + my_ext)
count_train = 0
for x in all_labels:
    if x not in val_test_list:
        ifile = os.path.basename(x)
        my_ext = os.path.splitext(ifile)[0]
        shutil.copy(x, TRAIN_LABEL_DIR.joinpath(ifile)) #Label
        shutil.copy(IMAGE_BASE.joinpath(my_ext + ".jpg"), TRAIN_IMAGE_DIR.joinpath(my_ext + ".jpg")) #Image
        # print("train: " + str(count_train) + ": " + my_ext)
        count_train += 1

print("complete")
# to start training
train_args = {
    'weights': WEIGHTS_FILE,
    'data': MODEL_FILE,
    'batch-size': BATCH_SIZE,
    'epochs': EPOCHS,
    'project': TRAINING_DATA,
    'exist_ok': True,
}

# # Actually run the training
# yolov5_train(**train_args)
# cd /usr/local/lib/python3.9/site-packages/yolov5
# python3 train.py --data coco_uavs.yml --batch-size 2 --weights weights.pt --img 640 --epochs 1
