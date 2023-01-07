import cv2
import json
from constants import CLS_NAMES
import numpy as np

import numpy as np


def cv_imread(path, gray=False):
    """For chinese read
    """
    im = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)
    if gray:
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    else:
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    return im

def load_img(img_path: str, binary=False) -> np.ndarray:
    
    if not binary:
        return cv_imread(img_path)
    else:
        im = cv_imread(img_path, gray=True)
        # Binarize
        _ , im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY)
        return im  
# def load_img(img_path: str, binary=False) -> np.ndarray:
    
#     if not binary:
#         return cv2.imread(img_path)
#     else:
#         im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         # Binarize
#         _ , im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY)
#         return im

def load_json_label(label_path: str) -> np.ndarray:
    """
    Return:
        a ndarray contains [x1, y1, x2, y2, cls_name]
    """
    with open(label_path, 'r') as f:
        data = json.load(f)
    rects = [label['points'] for label in data['shapes']]
    labels = [CLS_NAMES.index(label['label']) for label in data['shapes']]
    
    result = []
    for rect, label in zip(rects, labels):
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        rect = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2), label] # (x1, y1, x2, y2)
        result.append(rect)

    return np.array(result)