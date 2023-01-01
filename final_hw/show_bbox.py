import matplotlib.pyplot as plt
import cv2
import os
from os.path import join
import json
import numpy as np

if __name__ == '__main__':
    class_names = ['powder_uncover', 'powder_uneven', 'scratch']
    data_root = './data/raw'
    # new_data_root = './data/yolov5'
    data_split = 'Train'
    split_folder = join(data_root, data_split)
    # new_split_folder = join(new_data_root, data_split)
    name_idx = 0
    for cls_idx, cls_name in enumerate(class_names):
        img_folder = join(split_folder, cls_name, 'image')
        # mask_folder = join(split_folder, cls_name, 'mask')
        label_folder = join(split_folder, cls_name, 'label')
        for i, img_name in enumerate(os.listdir(img_folder)):
            if i == 5:
                break
            raw_name = img_name.split('.')[0]
            rgb_im = cv2.imread(join(img_folder, img_name))
            # mask_im = cv2.imread(join(mask_folder, img_name))
            labels = json.loads(open(join(label_folder, f'{raw_name}.json')).read())
            rects = [label['points'] for label in labels['shapes']]

            for c_i, rect in enumerate(rects):
                c_i = int((255 // len(rects)) * c_i)
                color = cv2.applyColorMap(np.array([c_i], dtype=np.uint8), cv2.COLORMAP_HSV).flatten()
                color = tuple([int(c) for c in color])
                image = cv2.rectangle(rgb_im, np.array(rect[0], dtype=int), np.array(rect[1], dtype=int), color, thickness=5)
            # Displaying the image 
            plt.figure(figsize=(12,12), tight_layout=True)
            plt.imshow(image)
            plt.show()
