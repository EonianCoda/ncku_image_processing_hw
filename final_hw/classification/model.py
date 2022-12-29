from torchvision.models import mobilenet_v3_large, mobilenet_v3_small
from torch.nn import Linear
import torch.nn as nn
import torch

def get_mobilenet_v3(num_classes: int, weight_path: str = None):
    # model = mobilenet_v3_large('MobileNet_V3_Large_Weights.IMAGENET1K_V2')
    model = mobilenet_v3_small('MobileNet_V3_Small_Weights.IMAGENET1K_V1')
    
    # Replace the final Linear layer
    our_linaer = Linear(1024, num_classes, bias=True)
    nn.init.normal_(our_linaer.weight, 0, 0.01)
    nn.init.zeros_(our_linaer.bias)
    model.classifier[3] = our_linaer

    if weight_path != None:
        param = torch.load(weight_path)
        model.load_state_dict(param)

    return model

def freeze_model(model):
    for name, param in model.named_parameters():
        if 'classifier' not in name:
            param.requires_grad = False

def unfreeze_model(model):
    for param in model.parameters():
        param.requires_grad = True