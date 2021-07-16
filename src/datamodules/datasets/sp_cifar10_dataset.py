import os
from typing import Callable, Optional

import numpy as np
import torch
from torch_geometric.data import InMemoryDataset
from torchvision.datasets import CIFAR10

from src.utils.superpixel_generation import convert_img_dataset_to_superpixel_graph_dataset


class CIFAR10SuperpixelsDataset(InMemoryDataset):
    """Dataset which converts CIFAR10 to dataset of superpixel graphs (on first run only)."""

    def __init__(
        self,
        data_dir: str = "data/",
        num_workers: int = 4,
        n_segments: int = 100,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        pre_filter: Optional[Callable] = None,
        **kwargs,
    ):
        self.data_dir = os.path.join(data_dir, "CIFAR10")
        self.num_workers = num_workers
        self.n_segments = n_segments
        self.slic_kwargs = kwargs

        super().__init__(self.data_dir, transform, pre_transform, pre_filter)

        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        """Dynamically generates filename for processed dataset based on superpixel parameters."""
        filename = ""
        filename += f"sp({self.n_segments})"
        for name, value in self.slic_kwargs.items():
            filename += f"_{name}({value})"
        filename += ".pt"
        return filename

    def process(self):
        trainset = CIFAR10(self.data_dir, train=True, download=True)
        testset = CIFAR10(self.data_dir, train=False, download=True)

        labels = np.concatenate((trainset.targets, testset.targets))
        images = np.concatenate((trainset.data, testset.data))

        data_list = convert_img_dataset_to_superpixel_graph_dataset(
            images=images,
            labels=labels,
            desired_nodes=self.n_segments,
            num_workers=self.num_workers,
        )

        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])
