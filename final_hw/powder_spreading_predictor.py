import sys
sys.path.extend(['./yolov5', './yolov5/utils'])
from yolov5.utils.metrics import box_iou, compute_ap

from yolov5_predictor import Yolov5_Predictor
from unet_predictor import UNet_Predictor
import cv2
import numpy as np
import torch

from constants import CLS_NAMES
from predictor_utils import load_json_label, load_img
import time


def compute_metric(pred: np.ndarray , gt: np.ndarray, ap_threshold = 0.5) -> dict:
    """
    Args:
        pred: a shape of (N, 6) ndarray, [x1, y1, x2, y2, conf, cls_idx]
        gt: a shape of (N, 5) ndarray, [x1, y1, x2, y2, cls_idx]
        ap_threshold: the thrshold for AP. Default is 0.5, which mean AP50.
    Return:
        a dict of (cls_idx, (AP, mean_iou))
    """
    # sort by conf
    conf_rank = np.argsort(pred[:, 4])[::-1]
    pred = pred[conf_rank]
    unique_cls = np.unique(pred[:,5])

    cls_result = dict()
    for cls_idx in unique_cls:
        cls_gt =  gt[gt[:,4] == cls_idx]
        cls_pred = pred[pred[:,5] == cls_idx]
        n_pred = len(cls_pred)
        n_gt = len(cls_gt)
        if len(cls_gt) == 0:
            cls_result[int(cls_idx)] = (np.zeros(n_pred), np.zeros(n_pred), 0.0)
            continue

        gt_box = cls_gt[:, :4]
        pred_box = cls_pred[:, :4]
        pred_conf = cls_pred[:, 4]
        ious = box_iou(torch.from_numpy(gt_box), torch.from_numpy(pred_box)).numpy()

        ious = ious.max(axis=0)
        mean_iou = np.mean(ious)
        true_target = ious > 0.5 # AP50

        TP = np.array([np.count_nonzero(true_target[:i+1]) for i in range(n_pred)])
        # FP = (np.arange(n_pred) + 1) - TP

        recall = TP / n_gt 
        precision = TP / (np.arange(n_pred) + 1)
        cls_name = CLS_NAMES[int(cls_idx)]
        cls_result[cls_name] = (recall, precision, mean_iou)


    for cls_name, (recall, precision, mean_iou) in cls_result.items():
        ap, _, _ = compute_ap(recall, precision)
        cls_result[cls_name] = (ap, mean_iou)
    return cls_result

def dice_coeff(input: np.ndarray, target: np.ndarray, epsilon: float = 1e-6) -> float:
    # Average of Dice coefficient for all batches, or for a single mask
    assert input.shape == target.shape
    assert len(input.shape) == 2

    _, input = cv2.threshold(input, 0, 1, cv2.THRESH_BINARY)
    input = input.astype(np.int32)
    _, target = cv2.threshold(target, 0, 1, cv2.THRESH_BINARY)
    target = target.astype(np.int32)

    inter = 2 * (input * target).sum()
    sets_sum = input.sum() + target.sum()
    sets_sum = np.where(sets_sum == 0, inter, sets_sum)

    dice = (inter + epsilon) / (sets_sum + epsilon)
    return np.mean(dice)

def draw_bbox(im, bboxes: np.ndarray) -> np.ndarray:
    if isinstance(im, str):
        im = load_img(im)
    lw = int(max(round(sum(im.shape) / 2 * 0.003), 2) * 1.5)
    txt_color = (220, 220, 220)
    box_color = (255, 0, 0)
    for box in bboxes:
        cls_idx = int(box[5])
        color = (255, 0, 0)
        # cv2.rectangle(im , (x1, y1), (x2, y2), bbox_color, 6, cv2.LINE_AA)
        
        p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
        cv2.rectangle(im, p1, p2, box_color, thickness=lw, lineType=cv2.LINE_AA)

        tf = max(lw - 1, 1)  # font thickness
        label = CLS_NAMES[cls_idx]
        w, h = cv2.getTextSize(label, 0, fontScale=lw / 3, thickness=tf)[0]  # text width, height
        outside = p1[1] - h >= 3
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        cv2.rectangle(im, p1, p2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(im,
                    label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                    0,
                    lw / 3,
                    txt_color,
                    thickness=tf,
                    lineType=cv2.LINE_AA)
    return im

class Powder_Spreading_Predictor(object):
    def __init__(self, yolo_weight_path:str, 
                        unet_weight_path:str,
                        bilinear=True,
                        crop_size=(320,320),
                        device:str = 'cpu'):
        self.yolov5_predictor = Yolov5_Predictor(yolo_weight_path, device=device)
        self.unet_predictor = UNet_Predictor(unet_weight_path, bilinear=bilinear, device=device)
        self.crop_size = crop_size

    def predict(self, img_path: str, mask_path:str, label_path: str):
        # Start to compute spending time
        start = time.time()
        metrics = dict()
        
        # Load image
        im = load_img(img_path)
        im_h, im_w , c = im.shape
        
        # Predict by yolov5
        pred_bboxes, crop_imgs, crop_box_infos = self.yolov5_predictor.predict_crop(img_path)

        # Not found any target in image
        if not isinstance(pred_bboxes, np.ndarray):
            metrics['detect'] = dict()
            metrics['pred_cls_name'] = 'None'
            metrics['dice'] = 0.0
            metrics['fps'] = 0.6
            pred_mask = np.zeros((im_h, im_w))
            return im, pred_mask, metrics
        
        pred_cls_idx = int(np.argmax(np.bincount(np.array(pred_bboxes[:, 5].astype(np.int64)), minlength = 3)))
        pred_cls_name = CLS_NAMES[pred_cls_idx]
        # Predict by UNet based on the result of yolov5
        pred_mask = np.zeros((im_h, im_w))
        
        
        if pred_cls_name == 'powder_uneven':
            invalid_idx = []

        for box_idx ,(crop_img, box_info) in enumerate(zip(crop_imgs, crop_box_infos)):
            box_w, box_h, x1, y1, x2, y2 = box_info

            origin_size = (box_w, box_h)
            # Resize the crop image into the input size of UNet
            resized_crop_img = cv2.resize(crop_img, self.crop_size) 
            unet_pred = self.unet_predictor.predict(cv2.cvtColor(resized_crop_img, cv2.COLOR_BGR2RGB), to_img=True) # Unet use Pillow, so we need to convert from BGR to RGB


            resize_unet_pred = cv2.resize(unet_pred, origin_size, interpolation=cv2.INTER_NEAREST)
            
            if pred_cls_name == 'powder_uneven':
                area = box_w * box_h
                seg_area = np.count_nonzero(resize_unet_pred)
                seg_ratio = seg_area / area
                if seg_ratio < 0.1:
                    invalid_idx.append(box_idx)
                    continue
            # Resize the result of predict img from UNet to origin size
            pred_mask[y1:y2, x1:x2] = resize_unet_pred
        
        if pred_cls_name == 'powder_uneven' and len(invalid_idx) != 0:
            ious = box_iou(torch.from_numpy(pred_bboxes[:, :4]), torch.from_numpy(crop_box_infos[:, 2:])).numpy()
            pred_target = np.argmax(ious, axis=1)

            valid_idx = np.ones(len(pred_bboxes))
            for idx in invalid_idx:
                for i in np.nonzero(pred_target == idx):
                    valid_idx[i] = 0
            pred_bboxes = pred_bboxes[valid_idx == 1]
        end = time.time()
        spending_time = end - start


        # Compute metrics
        gt_bboxes = load_json_label(label_path)
        metrics['detect'] = compute_metric(pred_bboxes, gt_bboxes)

        
        metrics['pred_cls_name'] = CLS_NAMES[pred_cls_idx]
        # Calculate dice coefficient
        gt_mask = load_img(mask_path, binary=True)
        metrics['dice'] = dice_coeff(pred_mask, gt_mask)
        metrics['fps'] = spending_time

        pred_img = draw_bbox(im, pred_bboxes)
        return pred_img, pred_mask, metrics
    