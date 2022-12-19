import json
import os
import shutil
import cv2
from utils import setup_logging
import logging
from tqdm import tqdm

logger = logging.getLogger()
def copy_file(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy(src , dst)

def gen_yolov5_txt(origin_h: float , 
                    origin_w: float,
                    label_file_path: str, 
                    txt_file_name: str, 
                    txt_file_root: str, 
                    cls_idx: int):
    with open(label_file_path, 'r') as f:
        data = json.load(f)

    os.makedirs(txt_file_root, exist_ok=True)
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
    with open(os.path.join(txt_file_root, txt_file_name), 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    setup_logging()
    class_names = ['powder_uncover', 'powder_uneven', 'scratch']
    raw_data_root = './data/raw'
    new_data_root = './data/yolov5'

    for split_name in ['Train', 'Val']:
        data_root = os.path.join(raw_data_root, split_name)
        new_data_root = os.path.join(new_data_root, split_name)

        name_idx = 0
        for cls_idx, cls in enumerate(class_names):
            cls_root = os.path.join(data_root, cls)
            for name in tqdm(os.listdir(os.path.join(cls_root, 'image'))):
                # Rename and move image
                new_name = f'{name_idx}.png'
                copy_file(os.path.join(cls_root, 'image', name), 
                        os.path.join(new_data_root, 'images', new_name))

                im = cv2.imread(os.path.join(new_data_root, 'images', new_name))
                h, w, c = im.shape
                txt_file_name = f'{name_idx}.txt'
                txt_file_root = os.path.join(new_data_root, 'label')
                label_file_path = os.path.join(cls_root, 'label', name.split('.')[0] + '.json')
                gen_yolov5_txt(h, w, label_file_path, txt_file_name, txt_file_root, cls_idx)
                name_idx += 1