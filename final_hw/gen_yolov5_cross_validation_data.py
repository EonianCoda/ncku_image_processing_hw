import os
from os.path import join
import shutil
from collections import defaultdict
import random
from tqdm import tqdm
def copy_file(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy(src , dst)

if __name__ == '__main__':
    class_names = ['powder_uncover', 'powder_uneven', 'scratch']
    random_seed = 123
    num_split = 4
    data_root = './data/yolov5/Train/'


    cls_imgs = defaultdict(list)
    for name in os.listdir(join(data_root, 'images')):
        for cls_name in class_names:
            if cls_name in name:
                cls_imgs[cls_name].append(name)
                break
    # Shuffle data
    for cls_name, img_names in cls_imgs.items():
        random.seed(random_seed)
        random.shuffle(img_names)
        cls_imgs[cls_name] = img_names
    
    # Split data
    for fold_idx in tqdm(range(num_split)):
        new_data_root = './data/fold{}'.format(fold_idx + 1)

        for img_names in cls_imgs.values():
            # Split data
            num_data = len(img_names)
            num_data_per_split = num_data // num_split
            
            val_start_idx = num_data_per_split * fold_idx
            if fold_idx == num_split - 1:
                val_end_idx = num_data
            else:
                val_end_idx = val_start_idx + num_data_per_split
            
            train_split = img_names[:val_start_idx] + img_names[val_end_idx:]
            val_split =  img_names[val_start_idx: val_end_idx]

            # Copy training data
            for img_name in train_split:
                raw_name = img_name.split('.')[0]
                txt_name = raw_name + '.txt'
                copy_file(join(data_root, 'images', img_name), join(new_data_root, 'Train', 'images', img_name))
                copy_file(join(data_root, 'masks', img_name), join(new_data_root, 'Train', 'masks', img_name))
                copy_file(join(data_root, 'labels', txt_name), join(new_data_root, 'Train', 'labels', txt_name))
                

            # Copy validating data
            for img_name in val_split:
                raw_name = img_name.split('.')[0]
                txt_name = raw_name + '.txt'
                copy_file(join(data_root, 'images', img_name), join(new_data_root, 'Val', 'images', img_name))
                copy_file(join(data_root, 'masks', img_name), join(new_data_root, 'Val', 'masks', img_name))
                copy_file(join(data_root, 'labels', txt_name), join(new_data_root, 'Val', 'labels', txt_name))