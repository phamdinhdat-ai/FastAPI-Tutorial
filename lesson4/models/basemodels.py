import torch
import torch.nn as nn 
import torch.nn.functional as F 
from torchvision.models import resnet152
import torch.optim as optim

class XModel(nn.Module):
    
    
    def __init__(self, config:object):
        super(XModel, self).__init__()
        self.n_classes = config.N_CLASSES 
        self.hidden_dim = config.HIDEEN_DIM 
        self.img_size = config.IMG_SIZE
    
    
        self.encoder =  None 
        self.fc = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.classifer = nn.Linear(self.hidden_dim, self.n_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.4)
    
    def forward(self, x):
        
        x = self.encoder(x)
        x = self.relu(x)
        x = self.fc(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.classifer(x)
        return x 
    
class XrayModel(nn.Module):
    def __init__(self, n_classes):
        super(XrayModel, self).__init__()
        
        resnet_model = resnet152(weights='ResNet152_Weights.DEFAULT')
        self.backbone = nn.Sequential(*list(resnet_model.children())[:-1])
        for params in self.backbone.parameters():
            params.requires_grad = False
        in_features = resnet_model.fc.in_features
        self.fc = nn.Linear(in_features, n_classes)
    
    def forward(self, x):
        x = self.backbone(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x
    
    def fit(self, train_dataloader, val_dataloader, learning_rate = 1e-3, weight_decay = 1e-5, num_epochs = 10):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.to(device)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.fc.parameters(), lr = learning_rate, weight_decay=weight_decay)
        
        for epoch in range(num_epochs):
            train_losses = []
            self.train()
            
            for images, labels in train_dataloader:
                # Move data to the correct device
                images = images.to(device)
                labels = labels.to(device)

                # Forward pass
                outputs = self(images)
                # Zero the parameter gradients
                optimizer.zero_grad()
                # Compute loss
                loss = criterion(outputs, labels)
                # Backward pass and optimize
                loss.backward()
                optimizer.step()
                train_losses.append(loss.item())
            train_loss = sum(train_losses) / len(train_losses)

            self.eval()
            val_losses = []
            correct_predictions = 0
            with torch.no_grad():
                for images, labels in val_dataloader:
                    # Move data to the correct device
                    images = images.to(device)
                    labels = labels.to(device)
                    
                    outputs = self(images)
                    loss = criterion(outputs, labels)
                    val_losses.append(loss.item())
                    
                    # Calculate accuracy
                    _, predicted = torch.max(outputs, 1)
                    correct_predictions += (predicted == labels).sum().item()
                    total_samples += labels.size(0)
            val_loss = sum(val_losses) / len(val_losses)
            val_accuracy = 100 * correct_predictions / total_samples
            # Print training and validation statistics
            print(f'Epoch {epoch+1}/{num_epochs}, \tTrain Loss: {train_loss:.3f}, \tVal Loss: {val_loss:.3f}, \tVal Accuracy: {val_accuracy:.3f}')
        
        print('Training complete!')