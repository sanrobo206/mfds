import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# ---- Step 1: Load and preprocess data ----
transform = transforms.Compose([
    transforms.ToTensor(),            # convert to tensor
    transforms.Normalize((0.5,), (0.5,))  # normalize between -1 and 1
])

train_data = datasets.MNIST(root='data', train=True, download=True, transform=transform)
test_data = datasets.MNIST(root='data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# ---- Step 2: Define a simple CNN model ----
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)   # (in_channels, out_channels, kernel_size)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.fc1 = nn.Linear(9216, 128)       # flatten layer output → dense
        self.fc2 = nn.Linear(128, 10)         # 10 classes (digits 0–9)

    def forward(self, x):
        x = F.relu(self.conv1(x))             # 1st conv + activation
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)  # 2nd conv + pooling
        x = torch.flatten(x, 1)               # flatten except batch dim
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleCNN()
print(model)

# Define optimizer and loss
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training loop
epochs = 3
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        optimizer.zero_grad()
        output = model(images)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")

model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        output = model(images)
        _, preds = torch.max(output, 1)
        total += labels.size(0)
        correct += (preds == labels).sum().item()

print(f"Test Accuracy: {100 * correct / total:.2f}%")
images, labels = next(iter(test_loader))
output = model(images)
_, preds = torch.max(output, 1)

fig, axes = plt.subplots(1, 6, figsize=(12, 3))
for i in range(6):
    axes[i].imshow(images[i].squeeze(), cmap='gray')
    axes[i].set_title(f"Pred: {preds[i].item()}")
    axes[i].axis('off')
plt.show()
torch.save(model.state_dict(), 'simple_cnn.pth')

