import json
import cv2
from albumentations import Normalize, Compose
from albumentations.pytorch.transforms import ToTensorV2
from torch.utils.data import Dataset, DataLoader

augment = Compose([
    Normalize(),
    ToTensorV2()
])
class EcgDataset2D(Dataset):
    def __init__(self, ann_path, mapping_path):
        super().__init__()
        self.data = json.load(open(ann_path))
        self.mapper = json.load(open(mapping_path))

    def __getitem__(self, index):
        img = cv2.imread(self.data[index]['path'])
        img = augment(**{"image": img})["image"]
        return {
            "image": img,
            "class": self.mapper[self.data[index]['label']]
        }

    def get_dataloader(self, batch_size=16, num_workers=4, shuffle=False):
        data_loader = DataLoader(
            self, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
        return data_loader

    def __len__(self):
        return len(self.data)


def callback_get_label(dataset, idx):
    return dataset[idx]["class"]

# if __name__ == "__main__":
    train = "data/train.json"
    mapping = "data/class-mapper.json"
    train_dl = EcgDataset2D(train,mapping).get_dataloader()
    for xb, xy in train_dl:
        pass

#         # cv2.imread()
#         # break
  
        

