import os
import shutil
import cv2
import numpy as np
from imantics import Polygons, Mask
def copy_file(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy(src , dst)

def gen_yolov7_txt(polygons:np.ndarray, cls:int, save_path: str):
    """
    Args:
        polygons: a array contain multiple line of [x1, y1, x2, y2, ... xn, yn]
        cls: the index of class
        save_path: A path for saving text file of yolov7 format 
    """
    lines = []
    for points in polygons:
        line = [str(cls)]
        line.extend([str(v) for v in points])
        line = ' '.join(line) + '\n'
        lines.append(line)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w') as f:
        f.writelines(lines)

def mask_to_polygons(mask_path: str) -> np.ndarray:
    im = cv2.imread(mask_path, 0)
    unique = np.unique(im)
    if len(unique) != 2:
        raise ValueError("Some Error in {}".format(mask_path))
    ret, im = cv2.threshold(im, unique[1] - 1, 255, cv2.THRESH_BINARY)
    h, w = im.shape
    polygons = Mask(im).polygons()

    normalized_points = []
    for points in polygons.points:
        points = points.astype(np.float32)
        points[..., 0] /= w # x
        points[..., 1] /= h # y
        points = points.reshape(-1)
        normalized_points.append(points)

    # Reshape into multuple line of [x1, y1, x2, y2, ... xn, yn]
    return normalized_points

if __name__ == "__main__":
    class_names = ['powder_uncover', 'powder_uneven', 'scratch']
    for split_name in ['Train', 'Val']:
        data_root = os.path.join('./origin_data', split_name)
        new_data_root = os.path.join('./data', split_name)

        name_idx = 0
        for cls_idx, cls in enumerate(class_names):
            cls_root = os.path.join(data_root, cls)
            for name in os.listdir(os.path.join(cls_root, 'image')):
                # Rename and move image
                new_name = f'{name_idx}.png'
                copy_file(os.path.join(cls_root, 'image', name), 
                        os.path.join(new_data_root, 'images', new_name))
                mask_path = os.path.join(cls_root, 'mask', name)

                yolov7_txt_path = os.path.join(new_data_root, 'labels', f"{name_idx}.txt")
                if not os.path.exists(yolov7_txt_path):
                    polygons = mask_to_polygons(mask_path)
                    gen_yolov7_txt(polygons, cls_idx, yolov7_txt_path)
                name_idx += 1