import json
import os
from os.path import join

import shutil
import cv2
from utils import setup_logging
import logging
from tqdm import tqdm
from multiprocessing import Pool
logger = logging.getLogger()
def copy_file(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy(src , dst)

def gen_yolov5_txt(origin_h: float , 
                    origin_w: float,
                    label_file_path: str, 
                    txt_file_path: str,
                    cls_idx: int):
    with open(label_file_path, 'r') as f:
        data = json.load(f)

    os.makedirs(os.path.dirname(txt_file_path), exist_ok=True)
    rects = [label['points'] for label in data['shapes']]
    lines = []
    for rect in rects:
        lt_x, lt_y = rect[0] # left top x, y
        rb_x, rb_y = rect[1] # right bottom x, y
        center_x = ((lt_x + rb_x) / 2) / origin_w
        center_y = ((lt_y + rb_y) / 2) / origin_h
        w, h = (rb_x - lt_x) / origin_w, (rb_y - lt_y) / origin_h
        w = abs(w)
        h = abs(h)

        line = [int(cls_idx), center_x, center_y, w, h]
        line = [str(element) for element in line]
        line = ' '.join(line) + '\n'
        lines.append(line)
    with open(txt_file_path, 'w') as f:
        f.writelines(lines)

def move_file_and_gen_txt(img_folder: str, 
                        label_folder: str, 
                        img_name: str,
                        new_split_folder: str,
                        new_name_idx: int,
                        cls_idx: int):
    raw_name = img_name.split('.')[0]

    # Rename and move image
    old_img_path = join(img_folder, img_name)
    new_img_path = join(new_split_folder, 'images', f'{new_name_idx}.png')
    copy_file(old_img_path, new_img_path)

    # Generate label txt
    im = cv2.imread(old_img_path)
    h, w, c = im.shape
    label_file_path = os.path.join(label_folder, f'{raw_name}.json')
    txt_file_path = join(new_split_folder, 'labels', f'{new_name_idx}.txt')
    gen_yolov5_txt(h, w, label_file_path, txt_file_path, cls_idx)


if __name__ == '__main__':
    setup_logging()
    class_names = ['powder_uncover', 'powder_uneven', 'scratch']
    data_root = './data/raw'
    new_data_root = './data/yolov5'
    with Pool(6) as p:
        for data_split in ['Train', 'Val']:
            split_folder = join(data_root, data_split)
            new_split_folder = join(new_data_root, data_split)
            name_idx = 0
            for cls_idx, cls_name in enumerate(class_names):
                img_folder = join(split_folder, cls_name, 'image')
                label_folder = join(split_folder, cls_name, 'label')
                for img_name in os.listdir(img_folder):
                    p.starmap(move_file_and_gen_txt, [(img_folder,
                                                        label_folder,
                                                        img_name,
                                                        new_split_folder,
                                                        name_idx, 
                                                        cls_idx)])
                    name_idx += 1