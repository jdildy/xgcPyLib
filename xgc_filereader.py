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

import adios2



import os
import re

class xgc1(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        print(str(self.xgc_path))
        self.vars = {}
        print("Reading XGC Output Data...")
        print("Getting Time Slice Data...")
        self.time = self.find_timeslice()
        print("TimeSlice Data Capture Complete.")

        
        self.length = len(self.time)

        self.step = self.time[1] - self.time[0]
        self.start = self.time[0] 
        self.end = self.time[-1] + self.step
        

        istart = self.start
        iend = self.end
        istep = self.step

        print(istart)
        print(iend)
        print(istep)
        
        print("Reading xgc.3d.xxxx.bp files...")
        for i in range(istart, iend, istep):
            filename = xgc_path + "/xgc.3d.%5.5d.bp" %(i)
            #print(filename)
            try:
                with Stream(filename,"rra") as f:
                    self.dpot = f.read("dpot")
                    self.dden = f.read('eden')
            except Exception as e:
                print(f"Error reading file: {e}")
        print("xgc.3d.xxxxx.bp files read sucessfully.")

        print(type(self.dpot))
        print(self.dpot)


        # print("Reading xgc.f3d.xxxx.bp files...")
        # for i in range(istart, iend, istep):
        #     filename = xgc_path + "/xgc.f3d.%5.5d.bp" %(i)
        #     #print(filename)
        #     try:
        #         with Stream(filename,"rra") as f:
        #             dpot = f.read("dpot")
        #             dden = f.read('eden')
        #     except Exception as e:
        #         print(f"Error reading file: {e}")
        # print("xgc.f3d.xxxxx.bp files read sucessfully.")









    def reader(self, file):
        try:
            with Stream(file, "rra") as f:
                for _ in f.steps():
                    self.vars = f.available_variables()
                    # # if isinstance(vars, dict):
                    # #     for name, info in vars.items():
                    # #         print("variable_name: " + name, end=" ")
                    #         # for key, value in info.items():
                    #         #     #print("\t" + key + ": " + value, end=" ")
                    #     print()
        except Exception as e:
            print(f"Error reading file: {e}")
        return self.vars
        




    def find_timeslice(self):
            path = self.xgc_path
            bp_timeslices = []

            pattern = re.compile(r'\b3d\.(\d+)\.bp\b')

            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for dir in dirs:
                        match = pattern.search(dir)
                        if match:
                            number = match.group(1)
                            #print(number)
                            bp_timeslices.append(number)
            else:
                print(f"The 'rundir' directory does not exist at path: {path}\n")
            
            print("Number of files found: " + str(len(bp_timeslices)))

            numbers = [int(item) for item in bp_timeslices]
            numbers.sort()
            # sorted_array = [f"{num:05d}" for num in numbers]
            # print(sorted_array) WORKS 
            return numbers








            
    
        

    # Call methods to demonstrate functionality


fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'


loader=xgc1(fileDir)
