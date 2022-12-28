from torchvision.models import mobilenet_v3_large
from torch.nn import Linear
import torch.nn as nn
def get_mobilenet_v3(num_classes: int):
    model = mobilenet_v3_large('MobileNet_V3_Large_Weights.IMAGENET1K_V2')

    # Replace the final Linear layer
    our_linaer = Linear(1280, num_classes, bias=True)
    nn.init.normal_(our_linaer.weight, 0, 0.01)
    nn.init.zeros_(our_linaer.bias)
    model.classifier[3] = our_linaer
    return model

def freeze_model(model):
    for name, param in model.named_parameters():
        if 'classifier' not in name:
            param.requires_grad = False

def unfreeze_model(model):
    for param in model.parameters():
        param.requires_grad = True