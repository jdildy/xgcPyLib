import numpy as np
import os
from adios2 import Stream

from tqdm.auto import tqdm
import glob

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

# Gets path from users and determines if it is a valid path or not
def checkpath(*args):
    if not args:
        raise ValueError("No path provided")
    
    file_path = args[0]

    
    if not os.path.isdir(file_path):
        raise ValueError(f"The path {file_path} is not a valid directory")
    
    file_path = os.path.join(file_path, '')
    return file_path




# Class handles all xgc.oneddiag.bp data

class data1(object):
    """
    XGC.ONEDDIAG Data Class

    This class handles the reading and returning of any value and its data pertaining to xgc.oneddiag.bp data

    INPUTS
    :param str xgc_pat: Name of the directory containing XGC Data
    """
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        #print(str(self.xgc_path))
        self.array_container = {}
        print("Reading xgc.oneddiag.bp Data...")
        
    # Reader for xgc.oneddiag.bp data
  
    def read_oneddiag(self,variable, s_start =None, s_count = None, dt= None, inds = Ellipsis):
        """
        read_oneddiag mehthod reads and returns based on the variable value

        INPUTS 
        :param str variable: variable from xgc.oneddiag to retrieve information from
        :param int s_start: Time step to start reading from 
        :param int s_count: Count of steps from s_start you want to read.
        :param int dt: Invertal between timesteps 

        Note: Not inputting s_start and s_count will read all available steps for that specific variable
        """
        try:
            with Stream(self.xgc_path + '/xgc.oneddiag.bp', 'rra') as r:
                if s_start != None and s_count != None: # Read all timestep data
                    if dt > 1: # catches dt greater than 1
                        start = (s_start -dt) / dt
                        start = int(start)
                        nsize = r.available_variables()[variable]['Shape']
                        if nsize != '': #mostly xgc.oneddiag
                            nsize = int(nsize)
                            data = r.read(variable,start=[0], count=[nsize],  step_selection=[start, s_count])
                        else: #scalar
                            data = r.read(variable,start=[], count=[], step_selection=[start, s_count])
                        return data
                    elif dt == 1:  
                        start = (s_start - 1)
                        nsize = r.available_variables()[variable]['Shape']
                        if nsize != '': #mostly xgc.oneddiag
                            nsize = int(nsize)
                            data = r.read(variable,start=[0], count=[nsize],  step_selection=[start, s_count])
                        else: #scalar
                            data = r.read(variable,start=[], count=[], step_selection=[start, s_count])
                            return data
                    return data
                else:
                    nstep = int(r.available_variables()[variable]['AvailableStepsCount'])
                    nsize = r.available_variables()[variable]['Shape']
                    if nsize != '': #mostly xgc.oneddiag
                        nsize = int(nsize)
                        data = r.read(variable,start=[0], count=[nsize],  step_selection=[0, nstep])
                    else: #scalar
                        data = r.read(variable,start=[], count=[], step_selection=[0, nstep])
        except Exception as e:
            print(f"Error in file: {e}\n")



# Class handles xgc.3d.xxxxx.bp or xgc.f3d.xxxxx.bp files
class xgc1(object):
    """
    XGC.3D.XXXXX.BP & XGC.F3D.XXXXX.BP Data Class

    This class handles the reading and returning of any value and its data pertaining to xgc1 data
    This class handles reading both 3D and F3D in one call, and deploys get functions to retrieve each variable

    INPUTS
    :param str xgc_pat: Name of the directory containing XGC Data
    """
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        self.array_containerF3D = {}
        self.array_container3D = {}
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
    

        istart = self.start 
        iend = self.end 
        istep = self.step 
        time = self.time 

        self.length = len(self.time)
        length = self.length



        print("Loading 3D File Info....")
        print("First Timestep: " + str(istart))
        print("Last Timestep: " + str(iend - istep))
        print("Step: " + str(istep))
        print("There are " + str(length) + " total steps available.")
    
        print("----------------------------------------\n")

        # choices = [
        #     (1, "Option 1: Read a single 3D data file"),
        #     (2, "Option 2: Read a range of 3D data files"),
        #     (3, "Option 3: Exit.")
        # ]
        # self.choice = user_select("Please choose an option:", choices)

        # if self.choice == 1:
        #     single = single_timestep(time)


        #     #XGC.3D.Reader
        #     print("Reading xgc.3d.%5.5d.bp..." %(single))
        #     filename = xgc_path + "/xgc.3d.%5.5d.bp" %(single)
            
        #     try:
        #         self.xgc1_reader(filename)
        #         print("xgc.3d.%5.5d.bp read sucessfully.\n" %(single))
            
        #     except Exception as e:
        #         print(f"Error reading file: {e}\n")
        
        #     #XGC.F3D.Reader 
        #     print("Reading xgc.f3d.%5.5d.bp files..." %(single))
        #     filename = xgc_path + "/xgc.f3d.%5.5d.bp" %(single)

        #     try:
        #         self.xgc1_reader(filename)
        #         print("xgc.f3d.%5.5d.bp read sucessfully.\n" %(single))
        #     except Exception as e:
        #         print(f"Error reading file: {e}\n")
        




        # elif self.choice == 2:
        #     start, end = mult_timestep(time)

        #     #Used in test.py
        #     self.input_start = start
        #     self.input_end = end


        #     print(f"Selected starting timestep: {start}\n")
        #     print(f"Selected ending timestep: {end}\n")
        #     count = len(range(start, end + istep, istep))
        #     #Test 2 , 10 as input
        #     #print(count) # 5
        #     data3D = []
        #     dataF3D = []
        #     pbar = tqdm(range(start,end + istep,istep), desc="Reading Files")
        #     for i in pbar:
        #         try:
        #             stepdata3D = self.xgc1_readmult3D(xgc_path + '/xgc.3d.%5.5d.bp' %(i))
        #             data3D.append(stepdata3D)
        #             self.data3D = data3D
        #         except Exception as e:
        #             print(f"Error reading file: {e}\n")

        #         try:
        #             stepdataF3D= self.xgc1_readmultF3D(xgc_path + '/xgc.f3d.%5.5d.bp' %(i))
        #             dataF3D.append(stepdataF3D)
        #             self.dataF3D = dataF3D

        #         except Exception as e:
        #             print(f"Error reading file: {e}\n")
        #     # print(f"Length of data: {len(data)}")
        #     # print(data)
        #     # data = np.array(data)
        #     # print(f"Dimensions of data: {data.ndim}")
        #     # print(f"Shape of data: {data.shape}")


        # elif self.choice == 3: 
        #     print("Exit")
        #     return 
        # else:
        #     #default
        #     print("Error Occured")  

    # #Get selection input used in test.py
    # def get_choice(self):
    #     return self.choice
    


    # #Get start, end and step count, used in test.py
    # def get_timesteps(self):
    #     return self.input_start, self.input_end, self.step
    


    # Reader method for both F3D and 3D
    def xgc1_reader(self,file):
        """
        Reader for f3d and 3d data. Only needs to be called once so that the get functions can retrieve the data.

        INPUTS
        param: str file: Name of the f3d or 3d file being read.
        """
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
    """
    XGC 3D reader reads mulitple timesteps of data
    
    """
    def xgc1_readmult3D(self,name,start, end, istep): 
        stepdata = []
        j= 0
        if start != None and end != None and istep != None:
            pbar = tqdm(range(start,end + istep,istep), desc="Reading Files")
            for i in pbar:
                with Stream(self.xgc_path + '/xgc.3d.%5.5d.bp' %(i), 'rra') as r:
                    try:
                        variables_list = r.available_variables()
                        for var_name in variables_list:
                            if var_name == name:
                                var = r.read(var_name)
                                stepdata[j] = var
                                j+=1
                    except Exception as e:
                            print(f"Error reading file: {e}")
            return stepdata
        















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
    def get_mult3Data(self,name):
        if name in self.array_container3D:
            return np.array(self.array_container3D[str(name)])
    
    def get_multF3Data(self,name):
        if name in self.array_containerF3D:
            return np.array(self.array_containerF3D[str(name)])

    # Retreive the timeslice available
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


# Class handles xgc.2d.xxxxx.bp or xgc.f2d.xxxxx.bp files

class xgca(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        
        self.array_containerF2D = {}
        self.array_container2D = {}
        print("Gathering Time Slice Data...")


        self.time = self.xgca_timeslice()
        if not self.time:
            print("No 2D Timeslice data available. Reading other files.")
            return
        
        print("TimeSlice Data Capture Complete.\n")
        self.length = len(self.time)

        self.step = self.time[1] - self.time[0]
        self.start = self.time[0] 
        self.end = self.time[-1] + self.step
    

        istart = self.start 
        iend = self.end 
        istep = self.step 
        time = self.time 

        self.length = len(self.time)
        length = self.length



        print("Loading 2D File Info....")
        print("First Timestep: " + str(istart))
        print("Last Timestep: " + str(iend - istep))
        print("Step: " + str(istep))
        print("There are " + str(length) + " total steps available.")
    
        print("----------------------------------------\n")

        choices = [
            (1, "Option 1: Read a single 2D data file"),
            (2, "Option 2: Read a range of 2D data files"),
            (3, "Option 3: Exit.")
        ]
        self.choice = user_select("Please choose an option:", choices)

        if self.choice == 1:
            single = single_timestep(time)


            #XGC.3D.Reader
            print("Reading xgc.2d.%5.5d.bp..." %(single))
            filename = xgc_path + "/xgc.2d.%5.5d.bp" %(single)
           
            #print(filename)
            
            try:
                self.xgca_reader(filename)
                print("xgc.2d.%5.5d.bp read sucessfully.\n" %(single))
            
            except Exception as e:
                print(f"Error reading file: {e}\n")
        
            #XGC.F3D.Reader 
            print("Reading xgc.f2d.%5.5d.bp files..." %(single))
            filename = xgc_path + "/xgc.f2d.%5.5d.bp" %(single)

            try:
                self.xgca_reader(filename)
                print("xgc.f2d.%5.5d.bp read sucessfully.\n" %(single))
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
            data2D = []
            dataF2D = []
            pbar = tqdm(range(start,end + istep,istep), desc="Reading Files")
            for i in pbar:
                try:
                    stepdata2D = self.xgca_readmult2D(xgc_path + '/xgc.3d.%5.5d.bp' %(i))
                    data2D.append(stepdata2D)
                    self.data2D = data2D
                except Exception as e:
                    print(f"Error reading file: {e}\n")

                try:
                    stepdataF2D= self.xgca_readmultF2D(xgc_path + '/xgc.f3d.%5.5d.bp' %(i))
                    dataF2D.append(stepdataF2D)
                    self.dataF2D = dataF2D

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
    


    # Reader method for both F3D and 3D
    def xgca_reader(self,file): 
        if '.f3d.' in str(file).lower():
            try:
                with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_containerF2D[var_name] = np.array(var)
            except Exception as e:
                print(f"Error reading file: {e}")
        elif '.3d.' in file:
            try:
                with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_container2D[var_name] = np.array(var)
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            print("Error: Neither F3D or 3D data exists.")

    



    #Work in progress
    def xgca_readmult2D(self,file): 
        try:
            with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_container2D[var_name] = np.array(var)
            print(f"Reading {file} file sucessful.")
            return self.array_container2D
        except Exception as e:
                print(f"Error reading file: {e}")


    def xgca_readmultF2D(self,file): 
        try:
            with Stream(file, 'rra') as r:
                    variables_list = r.available_variables()
                    for var_name in variables_list:
                        var = r.read(var_name)
                        self.array_containerF2D[var_name] = np.array(var)
            print(f"Reading {file} file sucessful.")
            return self.array_containerF2D
        except Exception as e:
                print(f"Error reading file: {e}")





    # Create a function to list all variables in a specfic file
    def list2DVars(self):
        for name in self.array_container2D:
            print(name)

    def list_F2DVars(self):
        for name in self.array_containerF2D:
            print(name)




    
    def get_loadVarF2D(self, name):
        if name in self.array_containerF2D:
            return np.array(self.array_containerF2D[str(name)])
        else:
            print(f"Variable with name '{name}' not found.")

    def get_loadVar3D(self, name):
        if name in self.array_container2D:
            return np.array(self.array_container2D[str(name)])
        else:
            print(f"Variable with name '{name}' not found.")



    # Return list of timesteps if selecting multiple timesteps
    def get_mult2Data(self):
        return self.data2D
    
    def get_multF2Data(self):
        return self.dataF2D

    # Retreive the timeslice available
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

# General reader (can read anything other than heatdiag2 and shealthdiag)
class loader(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'') 
        self.array_container = {}


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


        
# Class handles xgc.sheathdiag.bp
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
                
            
                if nsize != '':
                    var = r.inquire_variable(variable)
                    ndim = var.shape
                    cdim = str(nsize) #1,471
                    numbers = cdim.split(',')
                    dim = [int(num) for num in numbers]
                  
                    # Check the Dimensions of the Data
                    if len(dim) == 1: 
                        nsize = int(nsize)
                        data = r.read(variable,start=[0], count=[nsize],  step_selection=[0, nstep])
                        print("1D")
                    elif len(dim) == 2: 
                        rows = var.shape()[0]
                        columns = var.shape()[1]
                        data = r.read(variable,start=[0,0], count=[rows, columns],  step_selection=[0, nstep])
                        print("2D")
                    else:
                        print("Error: Too many dimensions.")
                else: #scalar
                   data = r.read(variable,start=[], count=[], step_selection=[0, nstep])
                   print("scalar")
                return data
                
                # return data        
        except Exception as e:
            print(f"Error in file: {e}\n")
            print("This ran")

# class handles xgc.heatdiag.bp
class heatdiag(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        #print(str(self.xgc_path))
        self.array_container = {}
        print("Reading xgc.heatdiag2.bp data...")
        

    def read_heatdiag2(self,variable, inds = Ellipsis):
        try:
            with Stream(self.xgc_path + '/xgc.heatdiag2.bp', 'rra') as r:
                nstep = int(r.available_variables()[variable]['AvailableStepsCount'])
                nsize = r.available_variables()[variable]['Shape']
                
            
                if nsize != '':
                    var = r.inquire_variable(variable)
                    ndim = var.shape
                    cdim = str(nsize) #1,471
                    numbers = cdim.split(',')
                    dim = [int(num) for num in numbers]
                  
                    # Check the Dimensions of the Data
                    if len(dim) == 1: 
                        nsize = int(nsize)
                        data = r.read(variable,start=[0], count=[nsize],  step_selection=[0, nstep])
                        print("1D")
                    elif len(dim) == 2: 
                        rows = var.shape()[0]
                        columns = var.shape()[1]
                        data = r.read(variable,start=[0,0], count=[rows, columns],  step_selection=[0, nstep])
                        print("2D")
                    else:
                        print("Error: Too many dimensions.")
                else: #scalar
                   data = r.read(variable,start=[], count=[], step_selection=[0, nstep])
                   print("scalar")
                return data
                
                # return data        
        except Exception as e:
            print(f"Error in file: {e}\n")

#fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'

#required
#xgcaObj = xgca(fileDir)
# manager = loader(fileDir)adsfsdax
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
            
#heatObj = heatdiag(fileDir)
#heatObj.read_heatdiag2('ds')

# sheath_ilost = sheathObj.read_sheathdiag('sheath_ilost')
# print(type(sheath_ilost))
# print(sheath_ilost)
# print(sheath_ilost.shape)
# print(sheath_ilost.size)




#one_diagObj.read_oneddiag()


















