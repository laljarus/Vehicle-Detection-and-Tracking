# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 03:37:37 2018

@author: laljarus
"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
import time
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from skimage.feature import hog
from lesson_functions import *
import pickle
# NOTE: the next import is only valid for scikit-learn version <= 0.17
# for scikit-learn >= 0.18 use:
from sklearn.model_selection import train_test_split
from scipy.ndimage.measurements import label

from pathlib import Path

folder_path_cars = Path('./vehicles/')
vehicles_path = [x for x in folder_path_cars.iterdir() if x.is_dir()]
cars = []

for path in vehicles_path:
    images = path.glob('*.png')
    for image  in images:
        cars.append(str(image))


folder_path_noncars = Path('./non-vehicles/')
non_vehicles_path = [x for x in folder_path_noncars.iterdir() if x.is_dir()]
notcars = []

for path in non_vehicles_path:
    images = path.glob('*.png')
    for image in images:
        notcars.append(str(image))

# Reduce the sample size because
# The quiz evaluator times out after 13s of CPU time
sample_size = 8792
random_idx = np.random.randint(0,len(cars),sample_size)
cars = np.array(cars)[random_idx]
notcars = np.array(notcars)[0:sample_size]

### TODO: Tweak these parameters and see how the results change.
color_space = 'YCrCb' # Can be RGB, HSV, LUV, HLS, YUV, YCrCb
orient = 7  # HOG orientations
pix_per_cell = 8 # HOG pixels per cell
cell_per_block = 2 # HOG cells per block
hog_channel = "ALL" # Can be 0, 1, 2, or "ALL" or "gray"
spatial_size = (16, 16) # Spatial binning dimensions
hist_bins = 32    # Number of histogram bins
spatial_feat = True # Spatial features on or off
hist_feat = True # Histogram features on or off
hog_feat = True # HOG features on or off
y_start_stop = [350, 720] # Min and max in y to search in slide_window()

car_features = extract_features(cars, color_space=color_space, 
                        spatial_size=spatial_size, hist_bins=hist_bins, 
                        orient=orient, pix_per_cell=pix_per_cell, 
                        cell_per_block=cell_per_block, 
                        hog_channel=hog_channel, spatial_feat=spatial_feat, 
                        hist_feat=hist_feat, hog_feat=hog_feat)