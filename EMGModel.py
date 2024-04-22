import torch
import torch.nn as nn
import torch.nn.functional as F

class EMGModel(nn.Module):
    def __init__(self):
        super(EMGModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=2, padding=1)  # 32 filters, kernel size 3x3
        self.conv2 = nn.Conv2d(32, 64, kernel_size=2, padding=1)  # 64 filters, kernel size 3x3
        self.conv3 = nn.Conv2d(64, 128, kernel_size=2, padding=1)  # 128 filters, kernel size 3x3
        self.pool = nn.MaxPool2d(2)  # Max pooling layer with kernel size 2x2
        self.fc1 = nn.Linear(128 * 13 * 1, 128)  # Fully connected layer with 128 output features
        self.fc2 = nn.Linear(128, 2)  # Output layer with 2 classes for binary classification

    def forward(self, x):
        x = x.view(-1, 1, 100, 4)  # Reshape the input to (batch_size, channels, height, width)
        x = self.pool(torch.relu(self.conv1(x)))  # Apply convolution, then ReLU, then pooling
        x = self.pool(torch.relu(self.conv2(x)))  # Apply convolution, then ReLU, then pooling
        x = self.pool(torch.relu(self.conv3(x)))  # Apply convolution, then ReLU, then pooling
        x = x.view(-1, 128 * 13 * 1)  # Reshape the tensor for the fully connected layer
        x = torch.relu(self.fc1(x))  # Apply ReLU activation to the fully connected layer
        x = self.fc2(x)  # Output layer
        return x