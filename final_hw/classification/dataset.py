from torch.utils.data.dataset import Dataset
from PIL import Image
import os
import torch
import torch.nn as nn
from torchvision.transforms import transforms
import yaml
from torch.utils.data import DataLoader
class Transform(object):
    def __init__(self, is_train=True, img_size = (1024, 1024)):
        self.is_train = is_train
        self.img_size = img_size

    def __call__(self, im):
        im = transforms.Resize(self.img_size)(im)
        im = transforms.ToTensor()(im)
        return im

def get_transform(data_type="train"):
    if data_type == "train":
        transform = Transform(is_train=True)
    elif data_type == "test" or data_type == "val":
        transform = Transform(is_train=False)
    return transform

class Powder_Spreading_DataSet(Dataset):
    def __init__(self, img_root:str, 
                        label_file:str,
                        img_size = (1024, 1024),
                        is_train = True, 
                        cache = False, 
                        num_classes = 3) -> None:
        super().__init__()
        self.transform = Transform(is_train, img_size=img_size)
        
        with open(label_file, 'r') as f:
            lines = f.readlines()
        self.images = []
        self.labels = []
        
        for line in lines:
            file_name, cls = line.split(' ')
            self.images.append(os.path.join(img_root, file_name))
            self.labels.append(int(cls))
        
        self.cache = cache
        self.img_cache = dict()

        self.num_classes = num_classes
    def _read_img(self, path:str) -> torch.Tensor:
        im = Image.open(path).convert('RGB')
        return self.transform(im)

    def __len__(self) -> int:
        return len(self.images)
    def __getitem__(self, index: int):
        label = nn.functional.one_hot(torch.tensor(self.labels[index]), num_classes=self.num_classes)
        sample = {'label': label.float()}
        if self.cache:
            if index not in self.img_cache:
                im = self._read_img(self.images[index])
                self.img_cache[index] = im
            sample['img'] = self.img_cache[index].clone()
        else:
            sample['img'] = self._read_img(self.images[index])
        return sample

def get_dataloader(data_type='train', bs:int=16, **kwargs):
    data_type = data_type.lower()
    is_train = (data_type == 'train')

    with open('./data.yaml', 'r') as f:
        data = yaml.safe_load(f)

    if is_train:
        root, label_file = data['train_root'], data['train_label_file']
    else:
        root, label_file = data['val_root'], data['val_label_file']
    datadset = Powder_Spreading_DataSet(root, label_file, is_train=is_train, **kwargs)

    dataloader = DataLoader(datadset, batch_size=bs, num_workers=6, pin_memory=True, shuffle=is_train)

    return dataloader