import os
import sys
sys.path.append(os.path.abspath('./yolov5'))
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.augmentations import letterbox
from yolov5.models.experimental import attempt_load
import torch
import cv2
import numpy as np
from typing import Union, List
from os.path import join
from tqdm import tqdm
def load_img(img_path: str):
    return cv2.imread(img_path)

def load_binary_img(img_path: str):
    im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # Binarize
    _ , im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY)
    return im

def normalize_coord(coord: List[Union[int, float]], 
                    w: int, 
                    h: int, 
                    expand = 0):
    x1, y1, x2, y2 = [int(c) for c in coord]
    expand = int(expand)
    x1 = max(x1 - expand, 0)
    x2 = min(x2 + expand, int(w))
    y1 = max(y1 - expand, 0)
    y2 = min(y2 + expand, int(h))

    return [x1, y1, x2, y2]

class Yolov5_Predictor(object):
    def __init__(self, weight_path:str,
                        iou_thres = 0.6,
                        conf_thres = 0.1,
                        max_det = 1000,
                        img_size=(960, 960),
                        device='cpu') -> None:
        self.device = torch.device(device) if isinstance(device, str) else device

        # Initialize Model
        self.model = attempt_load(weights=weight_path, device=self.device, inplace=True, fuse=True)
        self.model = self.model.to(self.device)
        self.stride = max(int(self.model.stride.max()), 32)
        self.classes_names = self.model.names
        
        # Setting
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.max_det = max_det
        self.img_size = img_size
        self.crop_expand = {'scratch':10,
                            'powder_uneven':80,
                            'powder_uncover':80,}
    def predict(self, im0: Union[str, np.ndarray]):
        if isinstance(im0, str):
            im0 = load_img(im0)
        # im0 = cv2.imread(img_path)
        # Processing image
        im = letterbox(im0, self.img_size, stride=self.stride)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)
        im = torch.from_numpy(im).to(self.device)
        im = im.unsqueeze(dim=0) # add batch_size dimension
        im = im.float()  # uint8 to fp32
        im /= 255
        # Predict
        pred = self.model(im)
        # Process predictions
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, max_det=self.max_det)
        det = pred[0]
        if len(det):
            bboxs = []
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]
            for *xyxy, conf, cls in reversed(det):
                # xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                bboxs.append([int(cls), *xyxy]) # [cls, x1, y1, x2, y2]
            return bboxs
        else:
            return None

    def set_crop_expand(self, crop_expand:dict):
        if set(crop_expand.keys()) != set(self.classes_names):
            raise ValueError("The names of class in crop_expand should match the names of class in model")
        self.crop_expand = crop_expand

    def predict_crop(self, img_path:str, mask_path:str= None):
        im = load_img(img_path)
        im_h, im_w, c = im.shape
        bboxes = self.predict(im)

        crop_imgs = []
        box_infos = []

        if bboxes != None:
            total_area = im_h * im_w
            new_mask = np.zeros((im_h, im_w), dtype=np.uint8)
            for box in bboxes:
                cls_idx, x1, y1, x2, y2 = box
                cls_name = self.classes_names[cls_idx]
                expand = self.crop_expand[cls_name]
                # If the bbox is too small, then expand most.
                area = ((x2 - x1) * (y2 - y1)) / total_area

                cur_expand = expand * 2 if area <= 0.015 else expand
                x1, y1, x2, y2 = normalize_coord([x1, y1, x2, y2], im_w, im_h, expand=cur_expand)
                new_mask[y1:y2, x1:x2] = 255
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(new_mask, ltype=cv2.CV_16U)
            if num_labels >= 1:
               
                if mask_path != None:
                    mask = load_binary_img(mask_path)
                    crop_masks = []
                # Converted [x1, y1, w, h] to [x1, y1, x2, y2]
                stats[:,2] += stats[:,0]
                stats[:,3] += stats[:,1]

                for i in range(1, num_labels):
                    x1, y1, x2, y2, area = stats[i]
                    x1, y1, x2, y2 = normalize_coord([x1, y1, x2, y2], im_w, im_h)
                    box_w, box_h = (x2 - x1), (y2 - y1)
                    # Crop origin image and mask image
                    crop_im = im[y1:y2, x1:x2, ...]
                    crop_imgs.append(crop_im)
                    if mask_path != None:
                        crop_mask = mask[y1:y2, x1:x2]
                        crop_masks.append(crop_mask)
                    box_info = (box_w, box_h, x1, y1, x2, y2)
                    box_infos.append(box_info)
        
        if mask_path != None:
            return crop_imgs, crop_masks, box_infos
        else:
            return crop_imgs, box_infos

if __name__ == '__main__':
    num_fold = 4
    # for fold_idx in range(1, num_fold + 1):
    for fold_idx in range(1, 2):
        input_root = './data/yolov5_precise/'
        mask_root = './data/yolov5/'
        output_root = './data/unet_precise/'
        resize_size = (320, 320)

        img_size = (960, 960)
        weight_path = './yolov5/runs/train/precise_960_bs16_med_E300/weights/best.pt'
        iou_thres = 0.6
        conf_thres = 0.1
        predictor = Yolov5_Predictor(weight_path= weight_path,
                                    iou_thres=iou_thres,
                                    conf_thres=conf_thres,
                                    img_size=img_size,
                                    device='cuda')
        print("Start generate")
        for split in ['Train', 'Val']:
            input_split_folder = join(input_root, split)
            output_split_folder = join(output_root, split)

            input_img_folder = join(input_split_folder, 'images')
            input_mask_folder = join(mask_root, 'Train', 'masks')

            os.makedirs(join(output_split_folder, 'images'), exist_ok=True)
            os.makedirs(join(output_split_folder, 'masks'), exist_ok=True)
            os.makedirs(join(output_split_folder, 'labels'), exist_ok=True)
            for img_name in tqdm(os.listdir(input_img_folder)):
                raw_name = img_name.split('.')[0]
                img_path = join(input_img_folder, img_name)
                mask_path = join(input_mask_folder, img_name)

                crop_imgs, crop_masks, box_infos = predictor.predict_crop(img_path, mask_path)
                recover_lines = []
                # Write
                for crop_idx, (img, mask, box) in enumerate(zip(crop_imgs, crop_masks, box_infos)):
                    img = cv2.resize(img, resize_size)
                    mask = cv2.resize(mask, resize_size, interpolation=cv2.INTER_NEAREST)

                    new_name = '{}_{}.png'.format(raw_name, crop_idx)

                    cv2.imwrite(join(output_split_folder, 'images', new_name), img)
                    cv2.imwrite(join(output_split_folder, 'masks', new_name), mask)
                    # (box_w, box_h, x1, y1, x2, y2) for recover mask
                    box_line = ','.join([str(c) for c in box])
                    recover_lines.append(new_name + ',' + box_line + '\n')
                with open(join(output_split_folder, 'labels', '{}.txt'.format(raw_name)), 'w') as f:
                    f.writelines(recover_lines)