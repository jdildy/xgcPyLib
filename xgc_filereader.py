import numpy as np
import os
from matplotlib.tri import Triangulation, LinearTriInterpolator, CubicTriInterpolator
from adios2 import Stream
import matplotlib.pyplot as plt
from scipy.io import matlab
from scipy.optimize import curve_fit
from scipy.special import erfc
import scipy.sparse as sp
from tqdm.auto import trange, tqdm


import os
import re

class xgc1(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there

        print("Reading XGC Output Data...")
        print("Getting Time Slice Data...")
        #self.time = self.find_timeslice()
        print("TimeSlice Data Capture Complete.")




    def reader(self, file):
            with Stream(file, "rra") as f:
                for _ in f.steps():
                    for name, info in f.available_variables().items():
                        print("variable_name: " + name, end=" ")
                        for key, value in info.items():
                            print("\t" + key + ": " + value, end=" ")
                        print()

    def find_timeslice(self):
            path = self.path

            bp_timeslices = []

            pattern = re.compile(r'\b(?:3d|f3d)\.(\d+)\.bp\b')

            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for dir in dirs:
                        match = pattern.search(dir)
                        if match:
                            full_path = os.path.join(root, dir)
                            print(full_path)
                            bp_timeslices.append(full_path)
            else:
                print(f"The 'rundir' directory does not exist at path: {path}\n")
            
            return bp_timeslices
    
        

    # Call methods to demonstrate functionality


fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'


loader=xgc1(fileDir)
