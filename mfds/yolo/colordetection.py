import torch
import torch.nn as nn
import numpy as np
import cv2
from torch.utils.data import Dataset, DataLoader

class ShapesDataset(Dataset):
    def __init__(self, n=2000, size=64):
        self.data = []
        self.labels = []
        for _ in range(n):
            img = np.zeros((size, size 3), np.uint8)
            shape_type = np.random.choice(["circle", "square"])
            x, y = np.random.randint(10, size-20, 2)
            s = np.random.randint(5, 15)
            color = (255, 255, 255)
            if shape_type == "circle":
                cv2.circle(img)
