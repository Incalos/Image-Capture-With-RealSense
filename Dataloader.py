# -*- coding: UTF-8 -*-
"""
Author：Hefei Luo
"""
import json
import os
from pathlib import Path

import cv2
import numpy as np


class Intrinsics:
    def __init__(self, json_data):
        self.fx = json_data['fx']
        self.fy = json_data['fy']
        self.ppx = json_data['ppx']
        self.ppy = json_data['ppy']
        self.height = json_data['height']
        self.width = json_data['width']
        self.depth_scale = json_data['depth_scale']


class LoadImages:
    def __init__(self, path):
        if isinstance(path, str) and Path(path).suffix == '.txt':  # *.txt file with img/vid/dir on each line
            path = Path(path).read_text().rsplit()
        images_name = sorted([p for p in os.listdir(os.path.join(path, 'images'))], key=lambda x: eval(x.split('.')[0]))
        color_files = [os.path.join(os.path.join(path, 'images'), i) for i in images_name]
        depth_files = [os.path.join(os.path.join(path, 'DepthNpy'), i.split('.')[0] + '.npy') for i in images_name]
        self.nf = len(color_files)
        self.color_files = color_files
        self.depth_files = depth_files
        self.mode = 'image'
        with open(os.path.join(path, 'intrinsics.json'), 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
        self.intrinsics = Intrinsics(json_data)

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count == self.nf:
            raise StopIteration
        color_path = self.color_files[self.count]
        depth_path = self.depth_files[self.count]
        self.count += 1
        color_img = cv2.imread(color_path)
        depth_img = np.load(depth_path)/ self.intrinsics.depth_scale / 1000
        return color_img, depth_img, self.intrinsics

    def __len__(self):
        return self.nf
