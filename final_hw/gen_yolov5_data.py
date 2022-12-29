import json
import os
from os.path import join

import shutil
import cv2
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

        # if (w * h) < 0.013:
        #     max_w = min((1 - center_x) * 2, (center_x) * 2)
        #     max_h = min((1 - center_y) * 2, (center_y) * 2)
        #     w = min(max_w, w * 1.1)
        #     h = min(max_h, h * 1.1)

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
    class_names = ['powder_uncover', 'powder_uneven', 'scratch']
    # class_names = ['powder_uncover']
    data_root = './data/raw'
    new_data_root = './data/yolov5'
    move_mask = True
    # with Pool(6) as p:
    for data_split in ['Train', 'Val']:
        split_folder = join(data_root, data_split)
        new_split_folder = join(new_data_root, data_split)

        cls_name_indices = {i:0 for i in range(len(class_names))}
        for cls_idx, cls_name in enumerate(class_names):
            img_folder = join(split_folder, cls_name, 'image')
            label_folder = join(split_folder, cls_name, 'label')
            mask_folder = join(split_folder, cls_name, 'mask')

            for img_name in  tqdm(os.listdir(img_folder)):
                raw_name = img_name.split('.')[0]

                name_idx = cls_name_indices[cls_idx]
                # Rename and move image
                old_img_path = join(img_folder, img_name)
                new_img_path = join(new_split_folder, 'images', f'{cls_name}_{name_idx}.png')
                copy_file(old_img_path, new_img_path)

                # Move Mask
                if move_mask:
                    old_mask_path = join(mask_folder, img_name)
                    new_mask_path = join(new_split_folder, 'masks', f'{cls_name}_{name_idx}.png')
                    copy_file(old_mask_path, new_mask_path)

                # Generate label txt
                im = cv2.imread(old_img_path)
                h, w, c = im.shape
                label_file_path = os.path.join(label_folder, f'{raw_name}.json')
                txt_file_path = join(new_split_folder, 'labels', f'{cls_name}_{name_idx}.txt')
                gen_yolov5_txt(h, w, label_file_path, txt_file_path, cls_idx)

                cls_name_indices[cls_idx] += 1