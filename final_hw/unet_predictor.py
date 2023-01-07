from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F
from typing import Union
from UNet.utils.data_loading import BasicDataset
from UNet.unet import UNet

class UNet_Predictor(object):
    def __init__(self, weight_path:str,
                        scale = 0.5,
                        threshold=0.5,
                        n_classes=1,
                        bilinear=False,
                        device='cpu') -> None:
        self.device = torch.device(device) if isinstance(device, str) else device
        self.n_classes = n_classes
        # Initialize Model
        
        self.model = UNet(n_channels=3, n_classes=self.n_classes, bilinear=bilinear)
        self.model.to(device=device)
        state_dict = torch.load(weight_path, map_location=device)
        self.mask_values = state_dict.pop('mask_values')
        self.model.load_state_dict(state_dict)
        self.scale = scale
        self.threshold = threshold

    def predict(self, im0: Union[str, np.ndarray], to_img=False):
        if isinstance(im0, str):
            im0 = Image.open(im0)
        else:
            full_img = Image.fromarray(im0)

        self.model.eval()
        img = torch.from_numpy(BasicDataset.preprocess(None, 
                                                        full_img, 
                                                        self.scale, 
                                                        is_mask=False))
        img = img.unsqueeze(0)
        img = img.to(device=self.device, dtype=torch.float32)

        # Predict
        with torch.no_grad():
            output = self.model(img).cpu()
            output = F.interpolate(output, 
                                    (full_img.size[1], full_img.size[0]), 
                                    mode='bilinear')
            if self.n_classes > 1:
                mask = output.argmax(dim=1)
            else:
                mask = torch.sigmoid(output) > self.threshold

            mask = mask[0].long().squeeze().numpy()
        if to_img:
            return self.mask_to_image(mask)
        else:
            return mask

    def mask_to_image(self, mask: np.ndarray) -> np.ndarray:
        if isinstance(self.mask_values[0], list):
            out = np.zeros((mask.shape[-2], mask.shape[-1], len(self.mask_values[0])), dtype=np.uint8)
        elif self.mask_values == [0, 1]:
            out = np.zeros((mask.shape[-2], mask.shape[-1]), dtype=bool)
        else:
            out = np.zeros((mask.shape[-2], mask.shape[-1]), dtype=np.uint8)

        if mask.ndim == 3:
            mask = np.argmax(mask, axis=0)

        for i, v in enumerate(self.mask_values):
            out[mask == i] = v
        return out
