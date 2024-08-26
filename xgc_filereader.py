import numpy as np
import os
from matplotlib.tri import Triangulation, LinearTriInterpolator, CubicTriInterpolator
from adios2 import Stream, Variable
import matplotlib.pyplot as plt
from scipy.io import matlab
from scipy.optimize import curve_fit
from scipy.special import erfc
import scipy.sparse as sp
from tqdm.auto import trange, tqdm
from tabulate import tabulate

import adios2

import os
import re

def user_select( prompt, choices):
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
def mult_timestep(time):
        while True:
            try:
                stepSt = int(input("Enter the starting timestep: "))
                stepEd = int(input("Enter the ending timestep: "))

                if stepSt > stepEd:
                    print("The starting timestep must be less than the final ending timestep")
                    continue
                if stepSt == stepEd:
                    print("The timesteps selected can not be equal.")
                    continue
                if stepSt in time and stepEd in time:
                    return stepSt, stepEd
                else: 
                    print("Both timesteps must be apart of the timestep list. Try again.")
            except ValueError:
                print("Invalid inputs. Inputs must be numeric and cannot be letters.")       
def single_timestep(time):

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


# object for xgc.oneddiag.bp works
class data1(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        #print(str(self.xgc_path))
        self.array_container = {}
        print("Reading xgc.oneddiag.bp Data...")
        

    def read_oneddiag(self,variable, inds = Ellipsis):
        try:
            with Stream(self.xgc_path + '/xgc.oneddiag.bp', 'rra') as r:
                nstep = int(r.available_variables()[variable]['AvailableStepsCount'])
                nsize = r.available_variables()[variable]['Shape']
                if nsize != '': #mostly xgc.oneddiag
                    nsize = int(nsize)
                    data = r.read(variable,start=[0], count=[nsize],  step_selection=[0, nstep])
                else: #scalar
                    data = r.read(variable,start=[], count=[], step_selection=[0, nstep])

                return data
        except Exception as e:
            print(f"Error in file: {e}\n")



# Object for any xgc.3d.xxxxx.bp or xgc.f3d.xxxxx.bp file
class xgc1(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        print(str(self.xgc_path))
        self.array_containerF3D = {}
        self.array_container3D = {}
        print("Reading XGC Output Data:")
        print("Gathering Time Slice Data...")


        self.time = self.xgc1_timeslice()
        if not self.time:
            print("No 3D Timeslisces data available. Reading other files.")
            return
        
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
    
        print("----------------------------------------\n")

        choices = [
            (1, "Option 1: Read a single 3D data file"),
            (2, "Option 2: Read a range of 3D data files"),
            (3, "Option 3: Exit.")
        ]
        self.choice = user_select("Please choose an option:", choices)

        if self.choice == 1:
            single = single_timestep(time)


            #XGC.3D.Reader
            print("Reading xgc.3d.%5.5d.bp..." %(single))
            filename = xgc_path + "/xgc.3d.%5.5d.bp" %(single)
           
            #print(filename)
            
            try:
                self.xgc1_reader(filename)
                print("xgc.3d.%5.5d.bp read sucessfully.\n" %(single))
            
            except Exception as e:
                print(f"Error reading file: {e}\n")
        
            #XGC.F3D.Reader 
            print("Reading xgc.f3d.%5.5d.bp files..." %(single))
            filename = xgc_path + "/xgc.f3d.%5.5d.bp" %(single)

            try:
                self.xgc1_reader(filename)
                print("xgc.f3d.%5.5d.bp read sucessfully.\n" %(single))
            except Exception as e:
                print(f"Error reading file: {e}\n")
        
        elif self.choice == 2:
            start, end = mult_timestep(time)

            #Used in test.py
            self.input_start = start
            self.input_end = end


            print(f"Selected starting timestep: {start}\n")
            print(f"Selected ending timestep: {end}\n")
            count = len(range(start, end + istep, istep))
            #Test 2 , 10 as input
            #print(count) # 5
            data3D = []
            dataF3D = []
            pbar = tqdm(range(start,end + istep,istep), desc="Reading Files")
            for i in pbar:
                try:
                    stepdata3D = self.xgc1_readmult3D(xgc_path + '/xgc.3d.%5.5d.bp' %(i))
                    data3D.append(stepdata3D)
                    self.data3D = data3D
                except Exception as e:
                    print(f"Error reading file: {e}\n")

                try:
                    stepdataF3D= self.xgc1_readmultF3D(xgc_path + '/xgc.f3d.%5.5d.bp' %(i))
                    dataF3D.append(stepdataF3D)
                    self.dataF3D = dataF3D

                except Exception as e:
                    print(f"Error reading file: {e}\n")
            # print(f"Length of data: {len(data)}")
            # print(data)
            # data = np.array(data)
            # print(f"Dimensions of data: {data.ndim}")
            # print(f"Shape of data: {data.shape}")


        elif self.choice == 3: 
            print("Exit")
            return 
        else:
            #default
            print("Error Occured")  

    #Get selection input used in test.py
    def get_choice(self):
        return self.choice
    


    #Get start, end and step count, used in test.py
    def get_timesteps(self):
        return self.input_start, self.input_end, self.step
    



    def xgc1_reader(self,file): 
        if '.f3d.' in str(file).lower():
            try:
                with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_containerF3D[var_name] = np.array(var)
            except Exception as e:
                print(f"Error reading file: {e}")
        elif '.3d.' in file:
            try:
                with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_container3D[var_name] = np.array(var)
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            print("Error: Neither F3D or 3D data exists.")

    



    #Work in progress
    def xgc1_readmult3D(self,file): 
        try:
            with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_container3D[var_name] = np.array(var)
            print(f"Reading {file} file sucessful.")
            return self.array_container3D
        except Exception as e:
                print(f"Error reading file: {e}")


    def xgc1_readmultF3D(self,file): 
        try:
            with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_containerF3D[var_name] = np.array(var)
            print(f"Reading {file} file sucessful.")
            return self.array_containerF3D
        except Exception as e:
                print(f"Error reading file: {e}")





    # Create a function to list all variables in a specfic file
    def list3DVars(self):
        for name in self.array_container3D:
            print(name)

    def list_F3DVars(self):
        for name in self.array_containerF3D:
            print(name)




    # Retrieve a single variable and its data
    def get_loadVarF3D(self, name):
        if name in self.array_containerF3D:
            return np.array(self.array_containerF3D[str(name)])
        else:
            print(f"Variable with name '{name}' not found.")

    def get_loadVar3D(self, name):
        if name in self.array_container3D:
            return np.array(self.array_container3D[str(name)])
        else:
            print(f"Variable with name '{name}' not found.")



    # Return list of timesteps if selecting multiple timesteps
    def get_mult3Data(self):
        return self.data3D
    
    def get_multF3Data(self):
        return self.dataF3D

    # Retreive the timeslice
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





# Object for any xgc.2d.xxxxx.bp or xgc.f2d.xxxxx.bp file
class xgca(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        print(str(self.xgc_path))
        self.array_containerF2D = {}
        self.array_container2D = {}

        print("Gathering xgca (2D) Data:")
        print("Getting Time Slice Data...")
        self.time = self.xgca_timeslice()
        if not self.time:
            print("No 2D Timeslisce data available. Reading other files.")
            return
        self.time = self.xgca_timeslice()
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



        print("Loading 2D File Info....")
        print("First Timestep: " + str(istart))
        print("Last Timestep: " + str(iend - istep))
        print("Step: " + str(istep))
        print("There are " + str(length) + " total steps available.")
        print(type(self.time))
        print("----------------------------------------\n")

        choices = [
            (1, "Option 1: Read a single 2D data file"),
            (2, "Option 2: Read a range of 2D data files"),
            (3, "Option 3: Exit.")
        ]
        choice = user_select("Please choose an option:", choices)

        if choice == 1:
            single = single_timestep(time)
            #XGC.2D.Reader
            print("Reading xgc.2d.%5.5d.bp..." %(single))
            filename = xgc_path + "/xgc.2d.%5.5d.bp" %(single)
            
            try:
                self.xgca_reader(filename)
                
                    
                print("xgc.2d.%5.5d.bp read sucessfully." %(single))
            except Exception as e:
                print(f"Error reading file: {e}")
    

            #XGC.F2D.Reader
            print("Reading xgc.f2d.%5.5d.bp files..." %(single))
            filename = xgc_path + "/xgc.f2d.%5.5d.bp" %(single)
            try:
                self.xgca_reader(xgc_path + '/xgc.f2d.%5.5d.bp' %(single))
               
                
            except Exception as e:
                print(f"Error reading file: {e}")
        

        elif choice == 2:
            start, end = mult_timestep(time)
            print(f"Selected starting timestep: {start}")
            print(f"Selected ending timestep: {end}")

            pbar = tqdm(range(start,end + istep,istep), desc="Reading Files")
            
            for i in pbar:
                try:
                    self.xgca_reader(xgc_path + 'xgc2d.%5.5d.bp' %(i))
                   
                except Exception as e:
                    print(f"Error reading file: {e}")
                


                #XGC.F2D.Reader
                print("Reading xgc.f2d.%5.5d.bp files..." %(i))

                try:
                    self.xgca_reader(xgc_path + '/xgc.f2d.%5.5d.bp %' %(i))
                    
                except Exception as e:
                    print(f"Error reading file: {e}")
            print("Requested file read sucessful.\n")


        elif choice == 3: 
            print("Exit")
        else:
            #default
            print("Error Occured")

    def xgca_timeslice(self):
            path = self.xgc_path
            bp_timeslices = []

            pattern = re.compile(r'\b2d\.(\d+)\.bp\b')

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
    
    def xgca_reader(self, file):
        if '.f2d.' in str(file).lower():
            try:
                with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_containerF2D[var_name] = np.array(var)
            except Exception as e:
                print(f"Error reading file: {e}")
        elif '.2d.' in file:
            try:
                with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_container2D[var_name] = np.array(var)
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            print("Error: Neither F2D or 2D data exists.")


    def get_loadVar2D(self,name):
        if name in self.array_container2D:
            return self.array_container2D[str(name)]
        else:
            print(f"Variable with name '{name}' not found.")

    def get_loadVarF2D(self,name):
        if name in self.array_containerF2D:
            return self.array_containerF2D[str(name)]
        else:
            print(f"Variable with name '{name}' not found.")

# Object for reading files not dealing with timesteps 
# (can read anything other than heatdiag2 and shealthdiag)
class loader(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        #print(str(self.xgc_path)) # /pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun/
        self.array_container = {}
        #self.reader('xgc.grad_rz')


    # Can handle all General BP files except heatdiag2 and sheathdiag. Need to create tests to catch if 
    def reader(self, file):
        try:
            with Stream(self.xgc_path + file, 'rra') as r:
                variables_list = r.available_variables()
                for var_name in variables_list:
                    var = r.read(var_name)
                    self.array_container[var_name] = np.array(var)
            print(f"Reading {file} file sucessful.")
        except Exception as e:
            print(f"Error reading file: {e}")


    def get_loadVar(self,name):
        if name in self.array_container:
            return self.array_container[str(name)]
        else:
            print(f"Variable with name '{name}' not found.")

    def list_Vars(self, file):
        try:
            with Stream(self.xgc_path + file, 'rra') as r:
                variable_list = r.available_variables()
                for var_name in variable_list:
                    print(var_name + ", ", end=" ")
        except Exception as e:
            print(f"Error occured: {e}")


        
        
        

        




    # def readAdios(file,variable,inds = Ellipsis):
    #     if '/' in variable: variable = '/'+variable
    #         #v = '/'+v #this may be necessary for older xgc files

    #     " NEED SOME TYPE OF CHECKER TO ENSURE CORRECT FILE BEING OPENED"
    #     with Stream(str(file)+'.bp','rra') as r:
    #             if not isinstance(r, Stream):
    #                 raise TypeError("The object is not an instance of adios2.Stream")
                
    #             variables = r.available_variables()
                
    #             if variable not in variables:
    #                 raise KeyError(f"Variable '{variable}' not found in stream")
                
    #             nstep = int(variables[variable]['AvailableStepsCount'])
    #             nsize = variables[variable]['Shape']

    #             if nstep==1:
    #                 data = r.read(variable)[inds]
    #             elif nsize != '': #mostly xgc.oneddiag
    #                 nsize = int(nsize)
    #                 data = r.read(variable,start=[0], count=[nsize], step_start = 0, step_count = nstep)
    #             else: #mostly xgc.oneddiag
    #                 data = r.read(variable,start=[], count=[], step_start = 0, step_count=nstep)
    #     # except FileNotFoundError:
    #     #     print(f"File {file} not found.")
    #     # except TypeError as e:
    #     #     print(e)
    #     # except Exception as e: 
    #     #     print(f"An error has occured: {e}")  
    #             return data
        
# Object for sheath
class sheath(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        #print(str(self.xgc_path))
        self.array_container = {}
        print("Reading xgc.sheathdiag.bp data...")
        

    def read_sheathdiag(self,variable, inds = Ellipsis):
        try:
            with Stream(self.xgc_path + '/xgc.sheathdiag.bp', 'rra') as r:
                nstep = int(r.available_variables()[variable]['AvailableStepsCount'])
                nsize = r.available_variables()[variable]['Shape']
                print(nsize)
                
                cdim = str(nsize)
                array_count = cdim.split(',')
                array_count = [int(number.strip()) for number in array_count]

                print(array_count)
               
                # print(len(array_count))
                # if nsize != '':
                #     var = r.inquire_variable(variable)
                #     ndim = var.shape

                #     rows = var.shape()[0]
                #     columns = var.shape()[1]
                #     print(rows)
                #     print(columns)
                    

                #     if len(array_count) == 1: 
                #         nsize = int(nsize)
                #         data = r.read(variable,start=[0], count=[nsize],  step_selection=[0, nstep])
                #         print("1D")
                #     elif len(array_count) == 2: 
                #         nsize = int(nsize)
                #         data = r.read(variable,start=[0,0], count=[rows, columns],  step_selection=[0, nstep])
                #         print("2D")
                #     else:
                #         print("Error: Too many dimensions.")
                # else: #scalar
                #    data = r.read(variable,start=[], count=[], step_selection=[0, nstep])
                #    print("scalar")
                #return data
                
                # return data        
        except Exception as e:
            print(f"Error in file: {e}\n")
            print("This ran")

    

fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'

#required
#xgc1Obj = xgc1(fileDir)
#xgcaObj = xgca(fileDir)
# manager = loader(fileDir)
#data1Obj = data1(fileDir)

# manager.reader('/xgc.mesh.bp')

# rz = manager.get_loadVar('rz')
# print(rz)

#Testing
# i_radial_en_flux_ExB_turb_df = xgc1Obj.get_loadVar3D('i_radial_en_flux_ExB_turb_df')
# print(i_radial_en_flux_ExB_turb_df)
#data1Obj = data1(fileDir)

# time = data1Obj.get_oneddiag('time')
# psi = data1Obj.get_oneddiag('psi')
# tindex = data1Obj.get_oneddiag('tindex')
# step = data1Obj.get_oneddiag('step')

# print(time)
# print(psi)
# print(tindex)
# print(step)

#psi = data1Obj.get_oneddiag('psi')

#print(psi)


# xgc1Obj = xgc1(fileDir)









#psi = data1Obj.read_oneddiag('psi')
#print(psi)
#print(psi)








# hyp_vis_rad = manager.reader('xgc.hyp_vis_rad.bp')
# grad_rz = manager.reader('xgc.grad_rz.bp')

# n_r = manager.get_loadVar('n_r')
# print(n_r)
            
sheathObj = sheath(fileDir)
sheathObj.read_sheathdiag('nwall')

# sheath_ilost = sheathObj.read_sheathdiag('sheath_ilost')
# print(type(sheath_ilost))
# print(sheath_ilost)
# print(sheath_ilost.shape)
# print(sheath_ilost.size)




#one_diagObj.read_oneddiag()


















