import time
import torch
import torch.nn as nn
from tqdm import tqdm
from typing import Dict, List
from dataset import get_dataloader
from model import get_mobilenet_v3, freeze_model, unfreeze_model
from utils import add_weight_decay
torch.backends.cudnn.benchmark = True


# Hyper parameters
num_classes = 3
num_epoch = 20
batch_size = 32
lr = 1e-4
weight_decay = 1e-6
# warmup_epoch = 5
cache = True
img_size = (224, 224)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if __name__ == '__main__':
    # Initialize Model
    model = get_mobilenet_v3(num_classes=num_classes)
    model = model.to(device)
    # Initialize dataloader
    train_loader = get_dataloader('train', batch_size, num_classes=num_classes, cache=cache, img_size=img_size)
    val_loader = get_dataloader('val', batch_size, num_classes=num_classes, cache=cache, img_size=img_size)
    # Initialize Optimizer
    optimizer = torch.optim.Adam(add_weight_decay(model), lr = lr)
    # Loss function
    criterion = nn.CrossEntropyLoss(reduction='mean')
    
    for epoch in range(num_epoch):
        print(f'epoch = {epoch}')
        start_time = time.time()
        optimizer.zero_grad(set_to_none=True)
        train_losses = 0.0
        train_accs = 0.0
        # Training
        model.training = True

        # Freeze feature layer for warm up
        # if epoch < warmup_epoch:
        #     freeze_model(model)
        # else:
        #     unfreeze_model(model)
        freeze_model(model)
        for i, sample in enumerate(tqdm(train_loader)):
            img, label = sample['img'].to(device), sample['label'].to(device)
            outputs = model(img)
            loss = criterion(outputs, label)
            loss.backward()
            train_losses += loss.item()
            
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)

            # Calculate accuracy
            label = torch.argmax(label, dim=1).detach().cpu()
            predicted_label = torch.argmax(outputs, dim=1).detach().cpu()
            acc = (label == predicted_label).sum() / len(label)

            train_accs += acc
            del loss
        print('Training Loss : {:.4f}'.format(train_losses / len(train_loader)))
        print('Training Accuracy : {:.4f}'.format(train_accs / len(train_loader)))
        # Validation
        val_losses = 0.0
        val_accs = 0.0
        with torch.no_grad():
            model.eval()
            for sample in tqdm(val_loader):
                img, label = sample['img'].to(device), sample['label'].to(device)
                outputs = model(img)
                loss = criterion(outputs, label)
                val_losses += loss.item()

                # Calculate accuracy
                label = torch.argmax(label, dim=1).detach().cpu()
                predicted_label = torch.argmax(outputs, dim=1).detach().cpu()
                acc = (label == predicted_label).sum() / len(label)
                val_accs += acc
        print('Validating Loss : {:.4f}'.format(val_losses / len(val_loader)))
        print('Validating Accuracy : {:.4f}'.format(val_accs / len(val_loader)))

        torch.save(model.state_dict(), f'{epoch}.pt')