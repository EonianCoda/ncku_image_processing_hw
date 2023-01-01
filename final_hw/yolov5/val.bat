cd yolov5
python val.py --imgsz 640 --batch-size 16 --data mydataset_cross_val.yaml --task test --weights ./runs/train/640_bs32_medium_E200/weights/best.pt