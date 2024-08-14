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


#3D Diagnostic Reader
class xgc1(object): 
    def __init__(self):
        self.path = "/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun" + '/'

        def reader(self, file):
            with Stream(file, "rra") as f:
                for _ in f.steps():
                    for name, info in f.available_variables().items():
                        print("variable_name: " + name, end=" ")
                        for key, value in info.items():
                            print("\t" + key + ": " + value, end=" ")
                        print()

        def find_timeslice():
            path = self.path

            bp_timeslices = []

            pattern = re.compile(r'\b(?:3d|f3d)\.(\d+)\.bp\b')

            if os.path.exists(path):
                 for root, dirs, files in os.walk(path):
                    for dir in dirs: 
                        match = pattern.search(dir)
                        if match:
                            full_path = os.path.join(dir)
                            print(full_path)
                            bp_timeslices.append(full_path)
            else: 
                print(f"The 'rundir' directory does not exist at path: {rundir}\n")
            return bp_timeslices



            

            
        


        

        print("Reading XGC Output Data...")
        print("Getting Time Slice Data...")
        self.time = find_timeslice()
        print("TimeSlice Data Capture Complete.")
        

        # def findTimeSlices():
        #     """
        #     Searches .bp files by timeslices, denoted by xxxx in file name, i.e xgc.xxxx.bp

        #     Returns: 
        #         List[str]: A list of available times slices based on the timeslices in the query search.
        #     """
        #     path = os.path.dirname(os.getcwd())
        #     rundir = os.path.join(path, 'rundir')


        #     bp_timeslices = []
            
        #     pattern = re.compile(r'\b(?:2d|f2d)\.(\d+)\.bp\b')

        #     if os.path.exists(rundir):
        #         for root, dirs, files in os.walk(rundir):
        #             for dir in dirs: 
        #                     match = pattern.search(dir)
        #                     if match:
        #                         full_path = os.path.join(dir)
        #                         print(full_path)
        #                         bp_timeslices.append(full_path)
        #     else: 
        #         print(f"The 'rundir' directory does not exist at path: {rundir}\n")
        #     return bp_timeslices


        

    