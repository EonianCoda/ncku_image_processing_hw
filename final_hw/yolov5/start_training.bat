@echo off
set /p var=PleaseEnterFold:
python my_train.py --cache ram --imgsz 640 --batch-size 16 --data mydataset_fold%var%.yaml --epochs 300 --weights yolov5m.pt