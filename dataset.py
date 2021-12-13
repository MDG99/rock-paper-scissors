import os
import torch
import pandas as pd
import cv2
from torch.utils.data import Dataset


class get_dataset(Dataset):

    def __init__(self, csv_file, root, transform=None):
        self.annotations = pd.read_csv(os.path.join(root, csv_file))
        self.root_dir = root
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, item):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[item, 0])
        image = cv2.imread(img_path, cv2.IMREAD_COLOR)
        label = torch.tensor(int(self.annotations.iloc[item, 1]))

        if self.transform:
            image = self.transform(image)

        return image, label