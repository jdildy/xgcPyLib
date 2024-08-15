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
        time = self.time # list

        self.length = len(self.time)
        length = self.length

        print("Loading 3D File Info....")
        print("First Timestep: " + str(istart))
        print("Last Timestep: " + str(iend - istep))
        print("Step: " + str(istep))
        print("There are " + str(length) + " total steps available.")
        print(type(self.time))
        print("----------------------------------------\n")

        choices = [
            (1, "Option 1: Read a single 3D data file"),
            (2, "Option 2: Read a range of 3D data files"),
            (3, "Option 3: Exit.")
        ]
        choice = self.user_select("Please choose an option:", choices)

        if choice == 1:
            single = self.single_timstep(time)
            #XGC.3D.Reader
            print("Reading xgc.3d.%5.5d.bp..." %(single))
            filename = xgc_path + "/xgc.3d.%5.5d.bp" %(single)
            
            try:
                with Stream(filename,"rra") as f:
                    #2D Arrays # works
                    self.dpot = f.read("dpot") 
                    self.eden = f.read('eden') 
                    self.epara = f.read('epara') 
                    self.epsi = f.read('epsi') 
                    self.etheta = f.read('etheta') 
                    self.iden = f.read('iden')
                    self.shpot = f.read('shpot')

                    #1D Arrays
                    self.e_marker_den = f.read('e_marker_den')
                    self.i_marker_weight = f.read('i_marker_weight')
                    self.i_weight_variance = f.read('i_weight_variance')
                    self.i_marker_den = f.read('e_marker_den')
                    self.i_marker_weight = f.read('e_marker_weight')
                    self.i_weight_variance = f.read('e_weight_variance')
                    self.pot0 = f.read('pot0')
                    self.pot0m = f.read('pot0m')

            
                    #Scalar #works
                    self.iphi = f.read('iphi')
                    self.nnode = f.read('nnode')
                    self.nphi = f.read('nphi')
                    self.nwall = f.read('nwall')
                    self.sheath_nphi = f.read('sheath_nphi')
                    self.time = f.read('time')
                   



                    
                    

                    
                    
                    
                    
                    
                    
                    print("xgc.3d.%5.5d.bp read sucessfully." %(single))
            except Exception as e:
                print(f"Error reading file: {e}")
            


            # #XGC.F3D.Reader
            # print("Reading xgc.f3d.%5.5d.bp files..." %(single))
            # filename = xgc_path + "/xgc.f3d.%5.5d.bp" %(single)

            # try:
            #     with Stream(filename,"rra") as f:
            #         self.i_pol_n0_f0= f.read('i_poloidal_flow_n0_f0')
            #         self.e_pol_n0_f0= f.read('e_poloidal_flow_n0_f0')
            # except Exception as e:
            #     print(f"Error reading file: {e}")
            # print("Reading xgc.f3d.%5.5d.bp file sucessful." %(single))

            



        
        

        elif choice == 2:
            print("Select Range")

        elif choice == 3: 
            print("Exit")
        else:
            #default
            print("Error Occured")


        


    def single_timstep(self, time):

        while True:
            try:
                select = int(input("Enter a valid timestep: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
        
            if select in time:
                return select
            else:
                print("Timestep not found. Try again.")
                
            
            
                

    # def mult_timestep(self, choice1 choice2):

    def user_select(self, prompt, choices):
        print(prompt)
        for number, description in choices:
            print(f"{number}. {description}")
        while True:
            try:
                select = input("Select a choice: ")
                choice = int(select)

                if any(choice == number for number, _ in choices):
                    return choice
                else: 
                    print("Invalid choice. Please select a valid option")
            except:
                print("Invalid input. Please enter a number.")







    
        


       


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
            #print(type(numbers[0])) each element is of type int
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
