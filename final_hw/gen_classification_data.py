import os
from os.path import join
from tqdm import tqdm
import shutil

def copy_file(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy(src , dst)

def move_file(img_folder: str,  
                img_name: str,
                new_split_folder: str,
                new_name_idx: int):
    # Rename and move image
    old_img_path = join(img_folder, img_name)
    new_img_path = join(new_split_folder, 'images', f'{new_name_idx}.png')
    copy_file(old_img_path, new_img_path)


if __name__ == '__main__':
    class_names = ['powder_uncover', 'powder_uneven', 'scratch']
    data_root = './data/raw'
    new_data_root = './data/classification'

    
    for data_split in ['Train', 'Val']:
        cls_indices = []
        split_folder = join(data_root, data_split)
        new_split_folder = join(new_data_root, data_split)
        name_idx = 0
        for cls_idx, cls_name in enumerate(class_names):
            img_folder = join(split_folder, cls_name, 'image')
            label_folder = join(split_folder, cls_name, 'label')
            for img_name in tqdm(os.listdir(img_folder)):
                old_img_path = join(img_folder, img_name)
                new_img_path = join(new_split_folder, 'images', f'{name_idx}.png')
                if not os.path.exists(new_img_path):
                    copy_file(old_img_path, new_img_path)
                cls_indices.append('{}.png {}\n'.format(name_idx, cls_idx))
                name_idx += 1
        with open(join(new_split_folder, 'labels.txt'), 'w') as f:
            f.writelines(cls_indices)