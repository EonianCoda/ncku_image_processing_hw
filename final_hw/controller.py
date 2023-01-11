import PyQt5
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtCore import  QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

from UI import Ui_MainWindow
from constants import start_btn_styleSheet, stop_btn_styleSheet, CLS_NAMES
from powder_spreading_predictor import Powder_Spreading_Predictor
from predictor_utils import load_img
import os
from os.path import join
import cv2
import numpy as np
import time
from collections import defaultdict

IMG_FOLDER = 'image'
LABEL_FOLDER = 'label'
MASK_FOLDER = 'mask'
TARGET_FOLDERS =  [IMG_FOLDER, LABEL_FOLDER, MASK_FOLDER]

PRED_RESULT = './predict_result'

def format_metric(a: float):
    return '{:.1f}%'.format(a * 100)

def img2QPixmap(img: np.ndarray):
    # BGR Image
    if len(img.shape) == 3 and img.shape[-1] == 3:
        h, w,c = img.shape
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        bytesPerLine = 3 * w
        qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
    else:
        if len(img.shape) == 3:
            h, w, _ = img.shape
        else:
            h, w = img.shape
        # Gray Image
        bytesPerLine = w
        qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_Grayscale8)
    return QPixmap(qImg)

def gen_white_img():
    img = np.ones((350, 350, 3), dtype=np.uint8) * 255
    return img2QPixmap(img)

def is_valid_folder(folder:str):
    if not os.path.isdir(folder):
        return False
    sub_folders = os.listdir(folder)
    if len(sub_folders) != 3:
        return False
    for t in TARGET_FOLDERS:
        if t not in sub_folders:
            return False
    return True

def gen_data_pairs(folder: str):
    if not is_valid_folder(folder):
        raise ValueError("Please give valid folder which contain 'image', 'label' and 'mask'.")

    data_pairs = []
    for img_name in os.listdir(join(folder, IMG_FOLDER)):
        raw_name = img_name.split('.')[0]
        data_pairs.append((folder, raw_name))
    return data_pairs

class Loading_dialog(QtWidgets.QDialog):
    """Loading Dialog for starting server or stop server
    """

    def __init__(self, parent):
        super(Loading_dialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # self.setWindowTitle("啟動中")
        self.value = 0
        vbox = QtWidgets.QVBoxLayout(self)
        self.movie_label = QtWidgets.QLabel()
        self.movie = QtGui.QMovie("./UI_imgs/process_bar.gif")
        self.movie_label.setMovie(self.movie)
        self.movie_label.setScaledContents(True)
        self.movie.start()
        self.progress_label = QtWidgets.QLabel()
        self.progress_label.setText("等待中")

        vbox.addWidget(self.movie_label)
        vbox.addWidget(self.progress_label)

        self.setLayout(vbox)
        self.setStyleSheet("background-color:white;")

    def show(self, title:str, content:str) -> None:
        self.setWindowTitle(title)
        self.progress_label.setText(content)
        return super().show()


class Init_predictor_thread(QThread):
    def __init__(self, end_signal, **kwargs):
        super().__init__()
        self.end_signal = end_signal
        self.kwargs = kwargs
    def run(self):
        self.predictor = Powder_Spreading_Predictor(**self.kwargs)
        self.end_signal.emit()

class Sleep_thread(QThread):
    def __init__(self, end_signal, sleep_secs: int):
        super().__init__()
        self.end_signal = end_signal
        self.sleep_secs = sleep_secs
    def run(self):
        time.sleep(self.sleep_secs)
        self.end_signal.emit()

class Predict_thread(QThread):
    def __init__(self, predictor: Powder_Spreading_Predictor, 
                        data_pairs: list,
                        update_signal,
                        end_signal):
        super().__init__()
        self.predictor = predictor
        self.stop = False
        self.shutdown = False
        self.data_pairs = data_pairs
        self.update_signal = update_signal
        self.end_signal = end_signal
        self.cur_idx = 0
        # self.idle_secs = idle_secs
    def run(self):
        for pair_idx, pair in enumerate(self.data_pairs):
            if self.shutdown:
                self.end_signal.emit()
                return
            # self.cur_idx = pair_idx
            while self.stop:
                time.sleep(1)

            root, raw_name = pair
            img_name = raw_name + '.png'
            json_name = raw_name + '.json'

            img_path = join(root, IMG_FOLDER, img_name)
            label_path = join(root, LABEL_FOLDER, json_name)
            mask_path = join(root, MASK_FOLDER, img_name)
            pred_img, pred_mask, metrics = self.predictor.predict(img_path, mask_path, label_path)
            result = {'pred_img': pred_img,
                    'pred_mask': pred_mask,
                    'img_path': img_path,
                    'mask_path': mask_path,
                    'idx': pair_idx,
                    'metrics': metrics}
            while self.stop:
                time.sleep(1)
            self.update_signal.emit(result)
            # time.sleep(self.idle_secs)
        self.end_signal.emit()

class MainWindow(QtWidgets.QMainWindow):
    end_load_model_signal = QtCore.pyqtSignal()
    gen_result_signal = QtCore.pyqtSignal(dict)
    predict_thread_end_signal = QtCore.pyqtSignal()
    
    pause_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_component()
        self.img_dir = ''
        self.img_idx = -1

        self.data_pairs = []
        self.init_model_thread = None
        self.predictor = None
        self.in_predict = False
        self.in_pause = False
        self.stat = defaultdict(list)
        self.avg_stat = defaultdict(list)

        self.yolov5_weight = './yolov5_best.pt'
        self.unet_weight = './unet_best.pth'
        self.update_folder_and_weight()
    def update_folder_and_weight(self):
        self.ui.yolov5_weight_label.setText(self.yolov5_weight)
        self.ui.unet_weight_label.setText(self.unet_weight)
        self.ui.img_folder_label.setText(self.img_dir)
    def select_yolov5_weight(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                    "Open file",
                                                    "./",
                                                    "Weight Files (*.pt)")
        if filename == '':
            return
        self.yolov5_weight = filename
        self.update_folder_and_weight()
        if self.img_dir != '':
            self.ui.run_btn.setEnabled(True)
    def select_unet_weight(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                            "Open file",
                                            "./",
                                            "Weight Files (*.pth)")
        if filename == '':
            return
        self.unet_weight = filename
        self.update_folder_and_weight()
        if self.img_dir != '':
            self.ui.run_btn.setEnabled(True)
    def init_component(self):
        # Connect button
        self.ui.run_btn.clicked.connect(self.run)
        self.ui.select_image_btn.clicked.connect(self.load_img_folder)

        self.ui.next_btn.clicked.connect(self.next_img)
        self.ui.prev_btn.clicked.connect(self.prev_img)

        self.ui.select_yolov5_btn.clicked.connect(self.select_yolov5_weight)
        self.ui.select_unet_btn.clicked.connect(self.select_unet_weight)

        # Connect Signal
        self.end_load_model_signal.connect(self.end_load_model_event)
        self.predict_thread_end_signal.connect(self.end_predict_thread_event)
        self.gen_result_signal.connect(self.gen_result)
        self.pause_signal.connect(self.end_wait_pause_event)
        # Initialized Message box and loading dialog
        self.msg_box = QMessageBox(self)
        self.loading = Loading_dialog(self)
        self.clear_screen()

        self.ui.run_btn.setEnabled(False)
    
    def end_predict_thread_event(self):
        print("End of prediction")
        self.in_predict = False
        self.predict_thread = None

        self.in_pause = True
        self.ui.run_btn.setText('Start')
        self.ui.run_btn.setStyleSheet(start_btn_styleSheet)
        self.ui.run_btn.setEnabled(False)
        
        self.ui.select_image_btn.setEnabled(True)
        self.ui.select_yolov5_btn.setEnabled(True)
        self.ui.select_unet_btn.setEnabled(True)

        self.ui.prev_btn.setEnabled(True)
        self.ui.next_btn.setEnabled(True)

    def clear_screen(self):
        # Initialize image
        self.ui.origin_fig.setPixmap(gen_white_img())
        self.ui.origin_fig.setScaledContents(True)
        self.ui.det_fig.setPixmap(gen_white_img())
        self.ui.det_fig.setScaledContents(True)
        self.ui.seg_fig.setPixmap(gen_white_img())
        self.ui.seg_fig.setScaledContents(True)
        self.ui.gt_fig.setPixmap(gen_white_img())
        self.ui.gt_fig.setScaledContents(True)
        # Initialize label
        self.ui.image_name_label.setText('')
        # Single Image
        self.ui.image_idx_label.setText('')
        self.ui.fps_label.setText('')
        self.ui.iou_label.setText('')
        self.ui.dice_coff_label.setText('')
        self.ui.ap50_label.setText('')
        self.ui.total_spending_time_label.setText('')
        self.ui.cur_img_idx_label.setText('')
        # Folder(Mean)
        self.ui.ap50_scratch_label.setText('')
        self.ui.ap50_powder_uneven_label.setText('')
        self.ui.ap50_powder_uncover_label.setText('')
        self.ui.map50_label.setText('')
        self.ui.iou_avg_label.setText('')
        
        self.ui.dice_powder_uncover_label.setText('')
        self.ui.dice_powder_uneven_label.setText('')
        self.ui.dice_scratch_label.setText('')
        self.ui.dice_avg_label.setText('')

   
    def load_img_folder(self):
        img_dir = QFileDialog.getExistingDirectory(self, 'Select Directory', './')
        # User press cancel
        if not os.path.isdir(img_dir):
            return
        
        if is_valid_folder(img_dir):
            data_pairs = gen_data_pairs(img_dir)
        else:
            data_pairs = []
            for folder in os.listdir(img_dir):
                sub_path = join(img_dir, folder)
                if is_valid_folder(sub_path):
                    data_pairs.extend(gen_data_pairs(sub_path))
                else:
                    self.msg_box.warning(self, '無效資料夾', f"{img_dir}為無效資料夾, 請選擇有包含image, label, mask三個資料夾的資料夾路徑")
                    return

        # self.clear_screen()
        self.num_data = len(data_pairs)
        self.data_pairs = data_pairs
        self.img_dir = img_dir
        self.img_idx = 0
        self.finish_img_idx = 0
        self.ui.image_idx_label.setText('{}/{}'.format(0, self.num_data))

        self.ui.run_btn.setEnabled(True)
        self.ui.prev_btn.setEnabled(False)
        self.ui.next_btn.setEnabled(False)

        self.update_folder_and_weight()
    def end_load_model_event(self):
        self.predictor = self.init_model_thread.predictor
        self.loading.close()
        self.init_model_thread = None
        self.in_predict = True
        self.predict_thread = Predict_thread(self.predictor, 
                                            self.data_pairs, 
                                            self.gen_result_signal,
                                            self.predict_thread_end_signal)

        self.predict_thread.start()
    
    def init_predictor(self):
        self.init_model_thread = Init_predictor_thread(self.end_load_model_signal,
                                                        yolo_weight_path=self.yolov5_weight, 
                                                        unet_weight_path=self.unet_weight, 
                                                        device='cuda')
        self.init_model_thread.start()
        self.loading.show("訊息", '讀取模型中，請稍後')

    def run(self):
        # In the progress of loading model
        if self.init_model_thread != None:
            return

        # In Start
        if self.ui.run_btn.text() == 'Start':
            # Start Predict
            if not self.in_predict:
                # Not load folder
                if len(self.data_pairs) == 0:
                    self.msg_box.warning(self, '警告', '請先選擇有效資料夾')
                    return
                self.init_predictor()
                os.makedirs(join(PRED_RESULT, 'detect'), exist_ok=True)
                os.makedirs(join(PRED_RESULT, 'seg'), exist_ok=True)
                self.in_pause = False

                self.clear_screen()
                self.stat = defaultdict(list)
                self.avg_stat = defaultdict(list)
                self.img_idx = 0
                self.finish_img_idx = 0


                self.ui.select_image_btn.setEnabled(False)
                self.ui.select_yolov5_btn.setEnabled(False)
                self.ui.select_unet_btn.setEnabled(False)
            else:
                self.predict_thread.stop = False
                self.in_pause = False

            self.ui.prev_btn.setEnabled(False)
            self.ui.next_btn.setEnabled(False)
            self.ui.run_btn.setText('Stop')
            self.ui.run_btn.setStyleSheet(stop_btn_styleSheet)
        # In Stop
        else:
            # In predict, just stop for a moment
            if self.in_predict:
                self.start_wait_pause()
                return
            self.in_predict = False
            self.ui.run_btn.setText('Start')
            self.ui.run_btn.setStyleSheet(start_btn_styleSheet)

    def start_wait_pause(self):
        self.predict_thread.stop = True
        self.in_pause = True
        self.loading.show("訊息", '暫停預測中，請稍後')
        self.sleep_thread = Sleep_thread(self.pause_signal, 1)
        self.sleep_thread.start()

    def end_wait_pause_event(self):
        self.loading.close()
        self.in_pause = True
        
        self.ui.run_btn.setText('Start')
        self.ui.run_btn.setChecked(False)
        self.ui.run_btn.setStyleSheet(start_btn_styleSheet)

        self.ui.prev_btn.setEnabled(True)
        self.ui.next_btn.setEnabled(True)
    def next_img(self):
        if not self.in_pause or self.img_idx >= self.finish_img_idx:
            return
        
        self.img_idx += 1
        self.change_img()

        
    def prev_img(self):
        if not self.in_pause or self.img_idx <= 1:
            return
        self.img_idx -= 1
        self.change_img()

    def change_img(self):
       
        img_idx = self.img_idx - 1
        # Load img and show
        img_path = self.stat['img_path'][img_idx]
        mask_path = self.stat['mask_path'][img_idx]
        pred_img_path = self.stat['pred_img'][img_idx]
        pred_mask_path = self.stat['pred_mask'][img_idx]
        
        self.ui.origin_fig.setPixmap(img2QPixmap(load_img(img_path)))
        self.ui.det_fig.setPixmap(img2QPixmap(load_img(pred_img_path)))
        self.ui.seg_fig.setPixmap(img2QPixmap(load_img(pred_mask_path, binary=True)))
        self.ui.gt_fig.setPixmap(img2QPixmap(load_img(mask_path, binary=True)))
        # Update UI
        iou = self.stat['iou'][img_idx]
        dice = self.stat['dice'][img_idx]
        ap = self.stat['ap'][img_idx]
        self.ui.iou_label.setText(format_metric(iou))
        self.ui.dice_coff_label.setText(format_metric(dice))
        self.ui.ap50_label.setText(format_metric(ap))
        self.ui.image_name_label.setText(os.path.basename(img_path))
        self.ui.image_idx_label.setText("{}/{}".format(self.img_idx, self.num_data))

    def gen_result(self, data):
        pred_img = data['pred_img']
        # pred_mask = data['pred_mask']
        img_path = data['img_path']
        mask_path = data['mask_path']

        self.img_idx = data['idx'] + 1
        self.finish_img_idx = self.img_idx
        dice = data['metrics']['dice']
        metrics = data['metrics']
        # Process Metrics
        # Calculate iou and AP for each category
        mean_iou = []
        mean_ap = []
        for cls_name, (ap, iou) in metrics['detect'].items():
            self.avg_stat['ap_{}'.format(cls_name)].append(ap)
            mean_iou.append(iou)
            mean_ap.append(ap)
        mean_iou = np.mean(mean_iou)
        mean_ap = np.mean(mean_ap)
        self.avg_stat['avg_iou'].append(mean_iou)
        total_avg_iou = np.mean(self.avg_stat['avg_iou'])
        self.ui.iou_avg_label.setText(format_metric(total_avg_iou))

        self.avg_stat['dice_{}'.format(metrics['pred_cls_name'])].append(dice)
        self.avg_stat['fps'].append(metrics['fps'])


        self.stat['dice'].append(dice)
        self.stat['iou'].append(mean_iou)
        self.stat['ap'].append(mean_ap)
        
        # Image path
        pred_img_path = join(PRED_RESULT, 'detect', '{}.png'.format(data['idx']))
        pred_mask_path = join(PRED_RESULT, 'seg', '{}.png'.format(data['idx']))

        self.stat['img_path'].append(img_path)
        self.stat['mask_path'].append(mask_path)
        self.stat['pred_img'].append(pred_img_path)
        self.stat['pred_mask'].append(pred_mask_path)
        # Store the result of prediction

        
        cv2.imwrite(pred_img_path, cv2.cvtColor(cv2.resize(data['pred_img'], (350, 350)), cv2.COLOR_BGR2RGB))
        cv2.imwrite(pred_mask_path, cv2.resize(data['pred_mask'], (350, 350), cv2.INTER_NEAREST))

        ### Update Folder(Mean) ###
        # Calculate AP for each class and MAP
        map = 0
        avg_dice = 0
        for cls_name in CLS_NAMES:
            aps = self.avg_stat['ap_{}'.format(cls_name)]
            ap = sum(aps) / max(len(aps), 1)
            getattr(self.ui,'ap50_{}_label'.format(cls_name)).setText(format_metric(ap))
            map += ap
            cls_dices = self.avg_stat['dice_{}'.format(cls_name)]
            cls_dice = sum(cls_dices) / max(len(cls_dices), 1)
            getattr(self.ui,'dice_{}_label'.format(cls_name)).setText(format_metric(cls_dice))
            avg_dice += cls_dice
        
        map /= len(CLS_NAMES)
        avg_dice /= len(CLS_NAMES)
        self.ui.map50_label.setText(format_metric(map))
        self.ui.dice_avg_label.setText(format_metric(avg_dice))

        sum_spend = sum(self.avg_stat['fps']) 
        avg_fps = sum_spend / len(self.avg_stat['fps'])
        self.ui.total_spending_time_label.setText('{:.1f}s'.format(sum_spend))
        self.ui.fps_label.setText('{:.3f}'.format(1 / avg_fps))

       

        ### Update Sinlge Image
        self.ui.iou_label.setText(format_metric(mean_iou))
        self.ui.dice_coff_label.setText(format_metric(dice))
        self.ui.ap50_label.setText(format_metric(mean_ap))
        self.ui.image_name_label.setText(os.path.basename(img_path))
        self.ui.image_idx_label.setText("{}/{}".format(data['idx'] + 1, self.num_data))
        self.ui.cur_img_idx_label.setText("{}/{}".format(data['idx'] + 1, self.num_data))

        # ### Update Image ###
        self.ui.origin_fig.setPixmap(img2QPixmap(load_img(img_path)))
        self.ui.det_fig.setPixmap(img2QPixmap(pred_img))
        self.ui.seg_fig.setPixmap(img2QPixmap(load_img(pred_mask_path, binary=True)))
        self.ui.gt_fig.setPixmap(img2QPixmap(load_img(mask_path, binary=True)))