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
        print("Reading XGC Output Data:")
        print("Getting Time Slice Data...")
        self.time = self.xgc1_timeslice()
        print("TimeSlice Data Capture Complete.\n")
        self.length = len(self.time)

        self.step = self.time[1] - self.time[0]
        self.start = self.time[0] 
        self.end = self.time[-1] + self.step
    
        

        istart = self.start #2
        iend = self.end #2172
        istep = self.step #2

        self.length = len(self.time)
        length = self.length

        print("Loading File Info....")
        print("First Timestep: " + str(istart))
        print("Last Timestep: " + str(iend - istep))
        print("Step: " + str(istep))
        print("There are " + str(length) + " total steps available.")
        print("----------------------------------------")

    
        


        
        # #XGC.3D.Reader
        # print("Reading xgc.3d.xxxx.bp files...")
        # for i in range(istart, iend, istep):
        #     filename = xgc_path + "/xgc.3d.%5.5d.bp" %(i)
        #     #print(filename)
        #     try:
        #         with Stream(filename,"rra") as f:
        #             self.dpot = f.read("dpot")
        #             self.dden = f.read('eden')
        #     except Exception as e:
        #         print(f"Error reading file: {e}")
        # print("xgc.3d.xxxxx.bp files read sucessfully.")


        # #XGC.F3D.Reader
        # print("Reading xgc.f3d.xxxx.bp files...")
        # for i in range(istart, iend, istep):
        #     filename = xgc_path + "/xgc.f3d.%5.5d.bp" %(i)
        #     #print(filename)
        #     try:
        #         with Stream(filename,"rra") as f:
        #             self.i_pol_n0_f0= f.read('i_poloidal_flow_n0_f0')
        #             self.e_pol_n0_f0= f.read('e_poloidal_flow_n0_f0')
        #     except Exception as e:
        #         print(f"Error reading file: {e}")
        # print("xgc.f3d.xxxxx.bp files read sucessfully.")



    def xgc1reader(self, file):
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

    def xgc1_timeslice(self):
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



# class xgca(object):
#     def __init__(self,xgc_path):
#         self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
#         print(str(self.xgc_path))
#         self.vars = {}
#         print("Reading XGC Output Data...")
#         print("Getting Time Slice Data...")
#         self.time = self.xgca_timeslice()
#         print("TimeSlice Data Capture Complete.")

        
#         self.length = len(self.time)

#         self.step = self.time[1] - self.time[0]
#         self.start = self.time[0] 
#         self.end = self.time[-1] + self.step
        

#         istart = self.start #2
#         iend = self.end #2172
#         istep = self.step #2
        
#         #XGC.2D.Reader
#         print("Reading xgc.2d.xxxx.bp files...")
#         for i in range(istart, iend, istep):
#             filename = xgc_path + "/xgc.2d.%5.5d.bp" %(i)
#             #print(filename)
#             try:
#                 with Stream(filename,"rra") as f:
                    
#             except Exception as e:
#                 print(f"Error reading file: {e}")
#         print("xgc.2d.xxxxx.bp files read sucessfully.")


#         #XGC.F2D.Reader

#         print("Reading xgc.f2d.xxxx.bp files...")
#         for i in range(istart, iend, istep):
#             filename = xgc_path + "/xgc.f2d.%5.5d.bp" %(i)
#             #print(filename)
#             try:
#                 with Stream(filename,"rra") as f:
                    
#             except Exception as e:
#                 print(f"Error reading file: {e}")
#         print("xgc.f3d.xxxxx.bp files read sucessfully.")



#     def xgcareader(self, file):
#         try:
#             with Stream(file, "rra") as f:
#                 for _ in f.steps():
#                     self.vars = f.available_variables()
#                     # # if isinstance(vars, dict):
#                     # #     for name, info in vars.items():
#                     # #         print("variable_name: " + name, end=" ")
#                     #         # for key, value in info.items():
#                     #         #     #print("\t" + key + ": " + value, end=" ")
#                     #     print()
#         except Exception as e:
#             print(f"Error reading file: {e}")
#         return self.vars

#     def xgca_timeslice(self):
#             path = self.xgc_path
#             bp_timeslices = []

#             pattern = re.compile(r'\b2d\.(\d+)\.bp\b')

#             if os.path.exists(path):
#                 for root, dirs, files in os.walk(path):
#                     for dir in dirs:
#                         match = pattern.search(dir)
#                         if match:
#                             number = match.group(1)
#                             #print(number)
#                             bp_timeslices.append(number)
#             else:
#                 print(f"The 'rundir' directory does not exist at path: {path}\n")
            
#             print("Number of files found: " + str(len(bp_timeslices)))

#             numbers = [int(item) for item in bp_timeslices]
#             numbers.sort()
#             # sorted_array = [f"{num:05d}" for num in numbers]
#             # print(sorted_array) WORKS 
#             return numbers



fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'


loader=xgc1(fileDir)
