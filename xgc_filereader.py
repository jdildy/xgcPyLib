import numpy as np
import os
from matplotlib.tri import Triangulation, LinearTriInterpolator, CubicTriInterpolator
from adios2 import Stream, FileReader
import matplotlib.pyplot as plt
from scipy.io import matlab
from scipy.optimize import curve_fit
from scipy.special import erfc
import scipy.sparse as sp
from tqdm.auto import trange, tqdm


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

# object for xgc.oneddiag.bp
class data1(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        #print(str(self.xgc_path))
        self.array_container = {}
        print("Reading XGC Output Data:")
        filename = xgc_path + "/xgc.oneddiag.bp"

        # choices = [
        #     (1, "Option 1: Read a single 2D data file"),
        #     (2, "Option 2: Read a range of 2D data files"),
        #     (3, "Option 3: Exit.")
        # ]

        # choice = user_select("Please choose an option:", choices)

        # if choice == 1:
        #     single = single_timestep(time)

        
        try:
            with Stream(filename, "rra") as r:
                variables_list = r.available_variables()
                for var_name in variables_list:
                    var = r.read(var_name)
                    self.array_container[var_name] = np.array(var)
        except Exception as e:
            print(f"Error in file: {e}\n")
        

                        
                        

    


    # def readerdata1(self, file):
    #     try:
    #         with Stream(file, 'rra') as r: 
    #             variables_list = r.available_variables()

    #             nstep = int(variables_list)
                
    #             for var_name in variables_list:
    #                 var = r.read(var_name)
    #                 #self.array_container[var_name] = np.array(var)
    #         print("Variables size in oneddiag: " + str(len(self.array_container)))
    #     except Exception as e:
    #         print(f"Error reading file: {e}\n")

    def get_oneddiag(self, name):
        if name in self.array_container:
            return self.array_container[name]
        else:
            print(f"Variable '{name}' not found.")
            return None


        






 
class xgc1(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        print(str(self.xgc_path))
        self.array_container = {}
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
        print(type(self.time))
        print("----------------------------------------\n")

        choices = [
            (1, "Option 1: Read a single 3D data file"),
            (2, "Option 2: Read a range of 3D data files"),
            (3, "Option 3: Exit.")
        ]
        choice = user_select("Please choose an option:", choices)

        if choice == 1:
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
        
        elif choice == 2:
            start, end = mult_timestep(time)
            print(f"Selected starting timestep: {start}\n")
            print(f"Selected ending timestep: {end}\n")

            pbar = tqdm(range(start,end + istep,istep), desc="Reading Files")
            
            for i in pbar:
                try:
                    self.xgc1_reader(xgc_path + '/xgc.3d.%5.5d.bp' %(i))
                    
                except Exception as e:
                    print(f"Error reading file: {e}\n")

                try:
                    self.xgc1_reader(xgc_path + '/xgc.f3d.%5.5d.bp' %(i))
                    
                except Exception as e:
                    print(f"Error reading file: {e}\n")
        elif choice == 3: 
            print("Exit")
            return 
        else:
            #default
            print("Error Occured")


    def xgc1_reader(self,file): 
        try:
            with Stream(file, 'rra') as r:
                variables_list = r.available_variables()
                for var_name in variables_list:
                    var = r.read(var_name)
                    self.array_container[var_name] = np.array(var)
            print(f"Reading {file} file sucessful.")
        except Exception as e:
            print(f"Error reading file: {e}")
    
    #Work in progress
    def xgc1_readermult(self,file,time): 
        try:
            with Stream(file, 'rra') as r:
                variables_list = r.available_variables()
                for var_name in variables_list:
                    var = r.read(var_name)[time]
                    self.array_container[var_name] = np.array(var)[time]
            print(f"Reading {file} file sucessful.")
        except Exception as e:
            print(f"Error reading file: {e}")

    def get_loadVar3D(self, name):
        if name in self.array_container:
            return self.array_container[str(name)]
        else:
            print(f"Variable with name '{name}' not found.")






        
    
                
    
            
                

    


    







    
        


       


    # def xgc1reader(self, file):
    #     try:
    #         with Stream(file, "rra") as f:
    #             for _ in f.steps():
    #                 self.vars = f.available_variables()
    #                 # # if isinstance(vars, dict):
    #                 # #     for name, info in vars.items():
    #                 # #         print("variable_name: " + name, end=" ")
    #                 #         # for key, value in info.items():
    #                 #         #     #print("\t" + key + ": " + value, end=" ")
    #                 #     print()
    #     except Exception as e:
    #         print(f"Error reading file: {e}")
    #     return self.vars

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






class xgca(object):
    def __init__(self,xgc_path):
        self.xgc_path = os.path.join(xgc_path,'')  #get file_path, add path separator if not there
        print(str(self.xgc_path))
        self.array_container = {}
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
                #with Stream(filename,"rra") as f:
                    # #2D Numpy Arrays # works
                    # self.dpot = f.read("dpot") #
                    # self.eden = f.read('eden') #
                    # self.epsi = f.read('epsi') 
                    # self.etheta = f.read('etheta') #
                    # self.iden = f.read('iden') #
                    


                    # #1D Arrays 
                    # self.e_marker_den = f.read('e_marker_den') #
                    # self.i_mean_weight = f.read('i_mean_weight') #
                    # self.i_weight_variance = f.read('i_weight_variance') #
                    # self.i_marker_den = f.read('e_marker_den') #
                    # self.e_mean_weight = f.read('e_mean_weight') #
                    # self.e_weight_variance = f.read('e_weight_variance') #
                    # self.pot0 = f.read('pot0') #
                    # self.pot0m = f.read('pot0m') #

            
                    # #Scalar #works
                    # #self.iphi = f.read('iphi') No 2d
                    # self.nnode = f.read('nnode') #
                    # #self.nphi3d = f.read('nphi') NO 2D
                    # #self.nwall = f.read('nwall') NO 2D
                    # #self.sheath_nphi = f.read('sheath_nphi') NO 2D
                    # self.time2d = f.read('time') #
                    
                print("xgc.2d.%5.5d.bp read sucessfully." %(single))
            except Exception as e:
                print(f"Error reading file: {e}")
    

            #XGC.F2D.Reader
            print("Reading xgc.f2d.%5.5d.bp files..." %(single))
            filename = xgc_path + "/xgc.f2d.%5.5d.bp" %(single)
            try:
                self.xgca_reader(xgc_path + '/xgc.f2d.%5.5d.bp' %(single))
                # with Stream(filename,"rra") as f:
                #     #2D Numpy Array
                #     #e_works
                #     self.dpotf3d = f.read('dpot') #
                #     #self.e_ExB_enflux_en = f.read('e_ExB_enflux_en')
                #     #self.e_ExB_flux_en = f.read('e_ExB_flux_en')
                #     self.e_T_para = f.read('e_T_para') #
                #     self.e_T_perp = f.read('e_T_perp') #
                #     self.e_den = f.read('e_den') #
                #     #self.e_den_en = f.read('e_den_en')
                #     #self.e_energy_en = f.read('e_energy_en')
                #     self.e_u_para = f.read('e_u_para')  #
                #     #i_#works
                #     #self.i_ExB_enflux_en = f.read('i_ExB_enflux_en')
                #     #self.i_ExB_flux_en = f.read('i_ExB_flux_en')
                #     self.i_T_para = f.read('i_T_para')
                #     self.i_T_perp = f.read('i_T_perp')
                #     self.i_den = f.read('i_den')
                #     #self.i_den_en = f.read('i_den_en')
                #     #self.i_energy_en = f.read('i_energy_en')
                #     self.i_u_para = f.read('i_u_para') #


                #     #1D Numpy Array #works
                #     #e_ works
                #     self.e_parallel_flow_df = f.read('e_parallel_flow_df') #
                #     self.e_parallel_flow_f0 = f.read('e_parallel_flow_f0') #
                #     #self.e_parallel_flow_turb_df = f.read('e_parallel_flow_turb_df')
                #     #self.e_parallel_flow_turb_f0 = f.read('e_parallel_flow_turb_f0')
                #     self.e_poloidal_flow_df = f.read('e_poloidal_flow_df') #
                #     self.e_poloidal_flow_f0 = f.read('e_poloidal_flow_f0') #
                #     #self.e_poloidal_flow_turb_df = f.read('e_poloidal_flow_turb_df')
                #     #self.e_poloidal_flow_turb_f0 = f.read('e_poloidal_flow_turb_f0')
                #     self.e_rad_mom_flux_3db_df = f.read('e_rad_mom_flux_3db_df')
                #     self.e_rad_mom_flux_3db_f0 = f.read('e_rad_mom_flux_3db_f0')
                #     #self.e_rad_mom_flux_3db_turb_df = f.read('e_rad_mom_flux_3db_turb_df')
                #     #self.e_rad_mom_flux_3db_turb_f0 = f.read('e_rad_mom_flux_3db_turb_f0')
                #     self.e_rad_mom_flux_ExB_df = f.read('e_rad_mom_flux_ExB_df')
                #     self.e_rad_mom_flux_ExB_f0 = f.read('e_rad_mom_flux_ExB_f0')
                #     #self.e_rad_mom_flux_ExB_turb_df = f.read('e_rad_mom_flux_ExB_turb_df')
                #     #self.e_rad_mom_flux_ExB_turb_f0 = f.read('e_rad_mom_flux_ExB_turb_f0')
                #     self.e_rad_mom_flux_mag_df = f.read('e_rad_mom_flux_mag_df')
                #     self.e_rad_mom_flux_mag_f0 = f.read('e_rad_mom_flux_mag_f0')
                #     #self.e_rad_mom_flux_mag_turb_df = f.read('e_rad_mom_flux_mag_turb_df')
                #     #self.e_rad_mom_flux_mag_turb_f0 = f.read('e_rad_mom_flux_mag_turb_f0')
                #     self.e_radial_en_flux_3db_df = f.read('e_radial_en_flux_3db_df')
                #     self.e_radial_en_flux_3db_f0 = f.read('e_radial_en_flux_3db_f0')
                #     #self.e_radial_en_flux_3db_turb_df = f.read('e_radial_en_flux_3db_turb_df')
                #     #self.e_radial_en_flux_3db_turb_f0 = f.read('e_radial_en_flux_3db_turb_f0')
                #     self.e_radial_en_flux_ExB_df = f.read('e_radial_en_flux_ExB_df')
                #     self.e_radial_en_flux_ExB_f0 = f.read('e_radial_en_flux_ExB_f0')
                #     #self.e_radial_en_flux_ExB_turb_df = f.read('e_radial_en_flux_ExB_turb_df')     
                #     #self.e_radial_en_flux_ExB_turb_f0 = f.read('e_radial_en_flux_ExB_turb_f0')
                #     self.e_radial_en_flux_mag_df = f.read('e_radial_en_flux_mag_df')       
                #     self.e_radial_en_flux_mag_f0 = f.read('e_radial_en_flux_mag_f0')   
                #     #self.e_radial_en_flux_mag_turb_df = f.read('e_radial_en_flux_mag_turb_df')  
                #     #self.e_radial_en_flux_mag_turb_f0 = f.read('e_radial_en_flux_mag_turb_f0')
                #     self.e_radial_flux_3db_df = f.read('e_radial_flux_3db_df')           
                #     self.e_radial_flux_3db_f0 = f.read('e_radial_flux_3db_f0')  
                #     #self.e_radial_flux_3db_turb_df = f.read('e_radial_flux_3db_turb_df')   
                #     #self.e_radial_flux_3db_turb_f0 = f.read('e_radial_flux_3db_turb_f0')    
                #     self.e_radial_flux_ExB_df = f.read('e_radial_flux_ExB_df')          
                #     self.e_radial_flux_ExB_f0 = f.read('e_radial_flux_ExB_f0')        
                #     #self.e_radial_flux_ExB_turb_df = f.read('e_radial_flux_ExB_turb_df')        
                #     #self.e_radial_flux_ExB_turb_f0 = f.read('e_radial_flux_ExB_turb_f0')         
                #     self.e_radial_flux_mag_df = f.read('e_radial_flux_mag_df')        
                #     self.e_radial_flux_mag_f0 = f.read('e_radial_flux_mag_f0')          
                #     #self.e_radial_flux_mag_turb_df = f.read('e_radial_flux_mag_turb_df') 
                #     #self.e_radial_flux_mag_turb_f0 = f.read('e_radial_flux_mag_turb_f0')         
                #     self.e_radial_pot_en_flux_3db_df = f.read('e_radial_pot_en_flux_3db_df')    
                #     self.e_radial_pot_en_flux_3db_f0 = f.read('e_radial_pot_en_flux_3db_f0')    
                #     #self.e_radial_pot_en_flux_3db_turb_df = f.read('e_radial_pot_en_flux_3db_turb_df')  
                #     #self.e_radial_pot_en_flux_3db_turb_f0 = f.read('e_radial_pot_en_flux_3db_turb_f0') 
                #     self.e_radial_pot_en_flux_ExB_df = f.read('e_radial_pot_en_flux_ExB_df')    
                #     self.e_radial_pot_en_flux_ExB_f0 = f.read('e_radial_pot_en_flux_ExB_f0')   
                #     #self.e_radial_pot_en_flux_ExB0_turb_df = f.read('e_radial_pot_en_flux_ExB0_turb_df') 
                #     #self.e_radial_pot_en_flux_ExB0_turb_f0 = f.read('e_radial_pot_en_flux_ExB0_turb_f0') 
                #     #self.e_radial_pot_en_flux_ExBt_df = f.read('e_radial_pot_en_flux_ExBt_df')  
                #     #self.e_radial_pot_en_flux_ExBt_f0 = f.read('e_radial_pot_en_flux_ExBt_f0')   
                #     #self.e_radial_pot_en_flux_ExBt_turb_df = f.read('e_radial_pot_en_flux_ExBt_turb_df') 
                #     #self.e_radial_pot_en_flux_ExBt_turb_f0 = f.read('e_radial_pot_en_flux_ExBt_turb_f0') 
                #     self.e_radial_pot_en_flux_mag_df = f.read('e_radial_pot_en_flux_mag_df')   
                #     self.e_radial_pot_en_flux_mag_f0 = f.read('e_radial_pot_en_flux_mag_f0')    
                #     #self.e_radial_pot_en_flux_mag_turb_df = f.read('e_radial_pot_en_flux_mag_turb_df') 
                #     #self.e_radial_pot_en_flux_mag_turb_f0 = f.read('e_radial_pot_en_flux_mag_turb_f0')
                #     self.e_tor_ang_mom_df = f.read('e_tor_ang_mom_df')          
                #     self.e_tor_ang_mom_f0 = f.read('e_tor_ang_mom_f0')            
                #     #self.e_tor_ang_mom_turb_df = f.read('e_tor_ang_mom_turb_df')             
                #     #self.e_tor_ang_mom_turb_f0 = f.read('e_tor_ang_mom_turb_f0')         
                #     self.e_toroidal_flow_df = f.read('e_toroidal_flow_df')           
                #     self.e_toroidal_flow_f0 = f.read('e_toroidal_flow_f0')          
                #     #self.e_toroidal_flow_turb_df = f.read('e_toroidal_flow_turb_df')          
                #     #self.e_toroidal_flow_turb_f0 = f.read('e_toroidal_flow_turb_f0')

                #     #i_
                #     self.i_parallel_flow_df = f.read('i_parallel_flow_df') #
                #     self.i_parallel_flow_f0 = f.read('i_parallel_flow_f0') #
                #     #self.i_parallel_flow_turb_df = f.read('i_parallel_flow_turb_df')
                #     #self.i_parallel_flow_turb_f0 = f.read('i_parallel_flow_turb_f0')
                #     self.i_poloidal_flow_df = f.read('i_poloidal_flow_df') #
                #     self.i_poloidal_flow_f0 = f.read('i_poloidal_flow_f0') #
                #     #self.i_poloidal_flow_turb_df = f.read('i_poloidal_flow_turb_df')
                #     #self.i_poloidal_flow_turb_f0 = f.read('i_poloidal_flow_turb_f0')
                #     self.i_rad_mom_flux_3db_df = f.read('i_rad_mom_flux_3db_df')
                #     self.i_rad_mom_flux_3db_f0 = f.read('i_rad_mom_flux_3db_f0')
                #     #self.i_rad_mom_flux_3db_turb_df = f.read('i_rad_mom_flux_3db_turb_df')
                #     #self.i_rad_mom_flux_3db_turb_f0 = f.read('i_rad_mom_flux_3db_turb_f0')
                #     self.i_rad_mom_flux_ExB_df = f.read('i_rad_mom_flux_ExB_df')
                #     self.i_rad_mom_flux_ExB_f0 = f.read('i_rad_mom_flux_ExB_f0')
                #     #self.i_rad_mom_flux_ExB_turb_df = f.read('i_rad_mom_flux_ExB_turb_df')
                #     #self.i_rad_mom_flux_ExB_turb_f0 = f.read('i_rad_mom_flux_ExB_turb_f0')
                #     self.i_rad_mom_flux_mag_df = f.read('i_rad_mom_flux_mag_df')
                #     self.i_rad_mom_flux_mag_f0 = f.read('i_rad_mom_flux_mag_f0')
                #     #self.i_rad_mom_flux_mag_turb_df = f.read('i_rad_mom_flux_mag_turb_df')
                #     #self.i_rad_mom_flux_mag_turb_f0 = f.read('i_rad_mom_flux_mag_turb_f0')
                #     self.i_radial_en_flux_3db_df = f.read('i_radial_en_flux_3db_df')
                #     self.i_radial_en_flux_3db_f0 = f.read('i_radial_en_flux_3db_f0')
                #     #self.i_radial_en_flux_3db_turb_df = f.read('i_radial_en_flux_3db_turb_df')
                #     #self.i_radial_en_flux_3db_turb_f0 = f.read('i_radial_en_flux_3db_turb_f0')
                #     self.i_radial_en_flux_ExB_df = f.read('i_radial_en_flux_ExB_df')
                #     self.i_radial_en_flux_ExB_f0 = f.read('i_radial_en_flux_ExB_f0')
                #     #self.i_radial_en_flux_ExB_turb_df = f.read('i_radial_en_flux_ExB_turb_df')     
                #     #self.i_radial_en_flux_ExB_turb_f0 = f.read('i_radial_en_flux_ExB_turb_f0')
                #     self.i_radial_en_flux_mag_df = f.read('i_radial_en_flux_mag_df')       
                #     self.i_radial_en_flux_mag_f0 = f.read('i_radial_en_flux_mag_f0')   
                #     #self.i_radial_en_flux_mag_turb_df = f.read('i_radial_en_flux_mag_turb_df')  
                #     #self.i_radial_en_flux_mag_turb_f0 = f.read('i_radial_en_flux_mag_turb_f0')
                #     self.i_radial_flux_3db_df = f.read('i_radial_flux_3db_df')           
                #     self.i_radial_flux_3db_f0 = f.read('i_radial_flux_3db_f0')  
                #     #self.i_radial_flux_3db_turb_df = f.read('i_radial_flux_3db_turb_df')   
                #     #self.i_radial_flux_3db_turb_f0 = f.read('i_radial_flux_3db_turb_f0')    
                #     self.i_radial_flux_ExB_df = f.read('i_radial_flux_ExB_df')          
                #     self.i_radial_flux_ExB_f0 = f.read('i_radial_flux_ExB_f0')        
                #     #self.i_radial_flux_ExB_turb_df = f.read('i_radial_flux_ExB_turb_df')        
                #     #self.i_radial_flux_ExB_turb_f0 = f.read('i_radial_flux_ExB_turb_f0')         
                #     self.i_radial_flux_mag_df = f.read('i_radial_flux_mag_df')        
                #     self.i_radial_flux_mag_f0 = f.read('i_radial_flux_mag_f0')          
                #     #self.i_radial_flux_mag_turb_df = f.read('i_radial_flux_mag_turb_df') 
                #     #self.i_radial_flux_mag_turb_f0 = f.read('i_radial_flux_mag_turb_f0')         
                #     self.i_radial_pot_en_flux_3db_df = f.read('i_radial_pot_en_flux_3db_df')    
                #     self.i_radial_pot_en_flux_3db_f0 = f.read('i_radial_pot_en_flux_3db_f0')    
                #     #self.i_radial_pot_en_flux_3db_turb_df = f.read('i_radial_pot_en_flux_3db_turb_df')  
                #     #self.i_radial_pot_en_flux_3db_turb_f0 = f.read('i_radial_pot_en_flux_3db_turb_f0') 
                #     self.i_radial_pot_en_flux_ExB_df = f.read('i_radial_pot_en_flux_ExB_df')    
                #     self.i_radial_pot_en_flux_ExB_f0 = f.read('i_radial_pot_en_flux_ExB_f0')   
                #     #self.i_radial_pot_en_flux_ExB0_turb_df = f.read('i_radial_pot_en_flux_ExB0_turb_df') 
                #     #self.i_radial_pot_en_flux_ExB0_turb_f0 = f.read('i_radial_pot_en_flux_ExB0_turb_f0') 
                #     #self.i_radial_pot_en_flux_ExBt_df = f.read('i_radial_pot_en_flux_ExBt_df')  
                #     #self.i_radial_pot_en_flux_ExBt_f0 = f.read('i_radial_pot_en_flux_ExBt_f0')   
                #     #self.i_radial_pot_en_flux_ExBt_turb_df = f.read('i_radial_pot_en_flux_ExBt_turb_df') 
                #     #self.i_radial_pot_en_flux_ExBt_turb_f0 = f.read('i_radial_pot_en_flux_ExBt_turb_f0') 
                #     self.i_radial_pot_en_flux_mag_df = f.read('i_radial_pot_en_flux_mag_df')   
                #     self.i_radial_pot_en_flux_mag_f0 = f.read('i_radial_pot_en_flux_mag_f0')    
                #     #self.i_radial_pot_en_flux_mag_turb_df = f.read('i_radial_pot_en_flux_mag_turb_df') 
                #     #self.i_radial_pot_en_flux_mag_turb_f0 = f.read('i_radial_pot_en_flux_mag_turb_f0')
                #     self.i_tor_ang_mom_df = f.read('i_tor_ang_mom_df')          
                #     self.i_tor_ang_mom_f0 = f.read('i_tor_ang_mom_f0')            
                #     #self.i_tor_ang_mom_turb_df = f.read('i_tor_ang_mom_turb_df')             
                #     #self.i_tor_ang_mom_turb_f0 = f.read('i_tor_ang_mom_turb_f0')         
                #     self.i_toroidal_flow_df = f.read('i_toroidal_flow_df')           
                #     self.i_toroidal_flow_f0 = f.read('i_toroidal_flow_f0')          
                #     #self.i_toroidal_flow_turb_df = f.read('i_toroidal_flow_turb_df')          
                #     #self.i_toroidal_flow_turb_f0 = f.read('i_toroidal_flow_turb_f0')

 

                #     self.pot0 = f.read('pot0')

                    
                #     #Scalar
                #     # self.inode1m1 = f.read('inode1m1')
                #     # self.iphim1 = f.read('iphim1')
                #     # self.n_energy = f.read('n_energy')
                #     # self.ndata = f.read('ndata')
                #     self.nnode = f.read('nnode') #
                #     #self.nphif3d = f.read('nphi') 
                #     #self.step =  f.read('step') 
                #     self.timef2d = f.read('time') #
                
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
                    # with Stream(xgc_path + 'xgc.2d.%5.5d.bp' %(i),"rra") as f:
                    #     #2D Numpy Arrays # works
                    #     self.dpot = f.read("dpot") #
                    #     self.eden = f.read('eden') #
                    #     self.epsi = f.read('epsi') 
                    #     self.etheta = f.read('etheta') #
                    #     self.iden = f.read('iden') #
                        


                    #     #1D Arrays 
                    #     self.e_marker_den = f.read('e_marker_den') #
                    #     self.i_mean_weight = f.read('i_mean_weight') #
                    #     self.i_weight_variance = f.read('i_weight_variance') #
                    #     self.i_marker_den = f.read('e_marker_den') #
                    #     self.e_mean_weight = f.read('e_mean_weight') #
                    #     self.e_weight_variance = f.read('e_weight_variance') #
                    #     self.pot0 = f.read('pot0') #
                    #     self.pot0m = f.read('pot0m') #

                
                    #     #Scalar #works
                    #     #self.iphi = f.read('iphi') No 2d
                    #     self.nnode = f.read('nnode') #
                    #     #self.nphi3d = f.read('nphi') NO 2D
                    #     #self.nwall = f.read('nwall') NO 2D
                    #     #self.sheath_nphi = f.read('sheath_nphi') NO 2D
                    #     self.time2d = f.read('time') #
                except Exception as e:
                    print(f"Error reading file: {e}")
                


                #XGC.F2D.Reader
                print("Reading xgc.f2d.%5.5d.bp files..." %(i))

                try:
                    self.xgca_reader(xgc_path + '/xgc.f2d.%5.5d.bp %' %(i))
                    # with Stream(xgc_path + '/xgc.f2d.%5.5d.bp' %(i),"rra") as f:
                    #     #2D Numpy Array
                    #     #e_works
                    #     self.dpotf3d = f.read('dpot') #
                    #     #self.e_ExB_enflux_en = f.read('e_ExB_enflux_en')
                    #     #self.e_ExB_flux_en = f.read('e_ExB_flux_en')
                    #     self.e_T_para = f.read('e_T_para') #
                    #     self.e_T_perp = f.read('e_T_perp') #
                    #     self.e_den = f.read('e_den') #
                    #     #self.e_den_en = f.read('e_den_en')
                    #     #self.e_energy_en = f.read('e_energy_en')
                    #     self.e_u_para = f.read('e_u_para')  #
                    #     #i_#works
                    #     #self.i_ExB_enflux_en = f.read('i_ExB_enflux_en')
                    #     #self.i_ExB_flux_en = f.read('i_ExB_flux_en')
                    #     self.i_T_para = f.read('i_T_para')
                    #     self.i_T_perp = f.read('i_T_perp')
                    #     self.i_den = f.read('i_den')
                    #     #self.i_den_en = f.read('i_den_en')
                    #     #self.i_energy_en = f.read('i_energy_en')
                    #     self.i_u_para = f.read('i_u_para') #


                    #     #1D Numpy Array #works
                    #     #e_ works
                    #     self.e_parallel_flow_df = f.read('e_parallel_flow_df') #
                    #     self.e_parallel_flow_f0 = f.read('e_parallel_flow_f0') #
                    #     #self.e_parallel_flow_turb_df = f.read('e_parallel_flow_turb_df')
                    #     #self.e_parallel_flow_turb_f0 = f.read('e_parallel_flow_turb_f0')
                    #     self.e_poloidal_flow_df = f.read('e_poloidal_flow_df') #
                    #     self.e_poloidal_flow_f0 = f.read('e_poloidal_flow_f0') #
                    #     #self.e_poloidal_flow_turb_df = f.read('e_poloidal_flow_turb_df')
                    #     #self.e_poloidal_flow_turb_f0 = f.read('e_poloidal_flow_turb_f0')
                    #     self.e_rad_mom_flux_3db_df = f.read('e_rad_mom_flux_3db_df')
                    #     self.e_rad_mom_flux_3db_f0 = f.read('e_rad_mom_flux_3db_f0')
                    #     #self.e_rad_mom_flux_3db_turb_df = f.read('e_rad_mom_flux_3db_turb_df')
                    #     #self.e_rad_mom_flux_3db_turb_f0 = f.read('e_rad_mom_flux_3db_turb_f0')
                    #     self.e_rad_mom_flux_ExB_df = f.read('e_rad_mom_flux_ExB_df')
                    #     self.e_rad_mom_flux_ExB_f0 = f.read('e_rad_mom_flux_ExB_f0')
                    #     #self.e_rad_mom_flux_ExB_turb_df = f.read('e_rad_mom_flux_ExB_turb_df')
                    #     #self.e_rad_mom_flux_ExB_turb_f0 = f.read('e_rad_mom_flux_ExB_turb_f0')
                    #     self.e_rad_mom_flux_mag_df = f.read('e_rad_mom_flux_mag_df')
                    #     self.e_rad_mom_flux_mag_f0 = f.read('e_rad_mom_flux_mag_f0')
                    #     #self.e_rad_mom_flux_mag_turb_df = f.read('e_rad_mom_flux_mag_turb_df')
                    #     #self.e_rad_mom_flux_mag_turb_f0 = f.read('e_rad_mom_flux_mag_turb_f0')
                    #     self.e_radial_en_flux_3db_df = f.read('e_radial_en_flux_3db_df')
                    #     self.e_radial_en_flux_3db_f0 = f.read('e_radial_en_flux_3db_f0')
                    #     #self.e_radial_en_flux_3db_turb_df = f.read('e_radial_en_flux_3db_turb_df')
                    #     #self.e_radial_en_flux_3db_turb_f0 = f.read('e_radial_en_flux_3db_turb_f0')
                    #     self.e_radial_en_flux_ExB_df = f.read('e_radial_en_flux_ExB_df')
                    #     self.e_radial_en_flux_ExB_f0 = f.read('e_radial_en_flux_ExB_f0')
                    #     #self.e_radial_en_flux_ExB_turb_df = f.read('e_radial_en_flux_ExB_turb_df')     
                    #     #self.e_radial_en_flux_ExB_turb_f0 = f.read('e_radial_en_flux_ExB_turb_f0')
                    #     self.e_radial_en_flux_mag_df = f.read('e_radial_en_flux_mag_df')       
                    #     self.e_radial_en_flux_mag_f0 = f.read('e_radial_en_flux_mag_f0')   
                    #     #self.e_radial_en_flux_mag_turb_df = f.read('e_radial_en_flux_mag_turb_df')  
                    #     #self.e_radial_en_flux_mag_turb_f0 = f.read('e_radial_en_flux_mag_turb_f0')
                    #     self.e_radial_flux_3db_df = f.read('e_radial_flux_3db_df')           
                    #     self.e_radial_flux_3db_f0 = f.read('e_radial_flux_3db_f0')  
                    #     #self.e_radial_flux_3db_turb_df = f.read('e_radial_flux_3db_turb_df')   
                    #     #self.e_radial_flux_3db_turb_f0 = f.read('e_radial_flux_3db_turb_f0')    
                    #     self.e_radial_flux_ExB_df = f.read('e_radial_flux_ExB_df')          
                    #     self.e_radial_flux_ExB_f0 = f.read('e_radial_flux_ExB_f0')        
                    #     #self.e_radial_flux_ExB_turb_df = f.read('e_radial_flux_ExB_turb_df')        
                    #     #self.e_radial_flux_ExB_turb_f0 = f.read('e_radial_flux_ExB_turb_f0')         
                    #     self.e_radial_flux_mag_df = f.read('e_radial_flux_mag_df')        
                    #     self.e_radial_flux_mag_f0 = f.read('e_radial_flux_mag_f0')          
                    #     #self.e_radial_flux_mag_turb_df = f.read('e_radial_flux_mag_turb_df') 
                    #     #self.e_radial_flux_mag_turb_f0 = f.read('e_radial_flux_mag_turb_f0')         
                    #     self.e_radial_pot_en_flux_3db_df = f.read('e_radial_pot_en_flux_3db_df')    
                    #     self.e_radial_pot_en_flux_3db_f0 = f.read('e_radial_pot_en_flux_3db_f0')    
                    #     #self.e_radial_pot_en_flux_3db_turb_df = f.read('e_radial_pot_en_flux_3db_turb_df')  
                    #     #self.e_radial_pot_en_flux_3db_turb_f0 = f.read('e_radial_pot_en_flux_3db_turb_f0') 
                    #     self.e_radial_pot_en_flux_ExB_df = f.read('e_radial_pot_en_flux_ExB_df')    
                    #     self.e_radial_pot_en_flux_ExB_f0 = f.read('e_radial_pot_en_flux_ExB_f0')   
                    #     #self.e_radial_pot_en_flux_ExB0_turb_df = f.read('e_radial_pot_en_flux_ExB0_turb_df') 
                    #     #self.e_radial_pot_en_flux_ExB0_turb_f0 = f.read('e_radial_pot_en_flux_ExB0_turb_f0') 
                    #     #self.e_radial_pot_en_flux_ExBt_df = f.read('e_radial_pot_en_flux_ExBt_df')  
                    #     #self.e_radial_pot_en_flux_ExBt_f0 = f.read('e_radial_pot_en_flux_ExBt_f0')   
                    #     #self.e_radial_pot_en_flux_ExBt_turb_df = f.read('e_radial_pot_en_flux_ExBt_turb_df') 
                    #     #self.e_radial_pot_en_flux_ExBt_turb_f0 = f.read('e_radial_pot_en_flux_ExBt_turb_f0') 
                    #     self.e_radial_pot_en_flux_mag_df = f.read('e_radial_pot_en_flux_mag_df')   
                    #     self.e_radial_pot_en_flux_mag_f0 = f.read('e_radial_pot_en_flux_mag_f0')    
                    #     #self.e_radial_pot_en_flux_mag_turb_df = f.read('e_radial_pot_en_flux_mag_turb_df') 
                    #     #self.e_radial_pot_en_flux_mag_turb_f0 = f.read('e_radial_pot_en_flux_mag_turb_f0')
                    #     self.e_tor_ang_mom_df = f.read('e_tor_ang_mom_df')          
                    #     self.e_tor_ang_mom_f0 = f.read('e_tor_ang_mom_f0')            
                    #     #self.e_tor_ang_mom_turb_df = f.read('e_tor_ang_mom_turb_df')             
                    #     #self.e_tor_ang_mom_turb_f0 = f.read('e_tor_ang_mom_turb_f0')         
                    #     self.e_toroidal_flow_df = f.read('e_toroidal_flow_df')           
                    #     self.e_toroidal_flow_f0 = f.read('e_toroidal_flow_f0')          
                    #     #self.e_toroidal_flow_turb_df = f.read('e_toroidal_flow_turb_df')          
                    #     #self.e_toroidal_flow_turb_f0 = f.read('e_toroidal_flow_turb_f0')

                    #     #i_
                    #     self.i_parallel_flow_df = f.read('i_parallel_flow_df') #
                    #     self.i_parallel_flow_f0 = f.read('i_parallel_flow_f0') #
                    #     #self.i_parallel_flow_turb_df = f.read('i_parallel_flow_turb_df')
                    #     #self.i_parallel_flow_turb_f0 = f.read('i_parallel_flow_turb_f0')
                    #     self.i_poloidal_flow_df = f.read('i_poloidal_flow_df') #
                    #     self.i_poloidal_flow_f0 = f.read('i_poloidal_flow_f0') #
                    #     #self.i_poloidal_flow_turb_df = f.read('i_poloidal_flow_turb_df')
                    #     #self.i_poloidal_flow_turb_f0 = f.read('i_poloidal_flow_turb_f0')
                    #     self.i_rad_mom_flux_3db_df = f.read('i_rad_mom_flux_3db_df')
                    #     self.i_rad_mom_flux_3db_f0 = f.read('i_rad_mom_flux_3db_f0')
                    #     #self.i_rad_mom_flux_3db_turb_df = f.read('i_rad_mom_flux_3db_turb_df')
                    #     #self.i_rad_mom_flux_3db_turb_f0 = f.read('i_rad_mom_flux_3db_turb_f0')
                    #     self.i_rad_mom_flux_ExB_df = f.read('i_rad_mom_flux_ExB_df')
                    #     self.i_rad_mom_flux_ExB_f0 = f.read('i_rad_mom_flux_ExB_f0')
                    #     #self.i_rad_mom_flux_ExB_turb_df = f.read('i_rad_mom_flux_ExB_turb_df')
                    #     #self.i_rad_mom_flux_ExB_turb_f0 = f.read('i_rad_mom_flux_ExB_turb_f0')
                    #     self.i_rad_mom_flux_mag_df = f.read('i_rad_mom_flux_mag_df')
                    #     self.i_rad_mom_flux_mag_f0 = f.read('i_rad_mom_flux_mag_f0')
                    #     #self.i_rad_mom_flux_mag_turb_df = f.read('i_rad_mom_flux_mag_turb_df')
                    #     #self.i_rad_mom_flux_mag_turb_f0 = f.read('i_rad_mom_flux_mag_turb_f0')
                    #     self.i_radial_en_flux_3db_df = f.read('i_radial_en_flux_3db_df')
                    #     self.i_radial_en_flux_3db_f0 = f.read('i_radial_en_flux_3db_f0')
                    #     #self.i_radial_en_flux_3db_turb_df = f.read('i_radial_en_flux_3db_turb_df')
                    #     #self.i_radial_en_flux_3db_turb_f0 = f.read('i_radial_en_flux_3db_turb_f0')
                    #     self.i_radial_en_flux_ExB_df = f.read('i_radial_en_flux_ExB_df')
                    #     self.i_radial_en_flux_ExB_f0 = f.read('i_radial_en_flux_ExB_f0')
                    #     #self.i_radial_en_flux_ExB_turb_df = f.read('i_radial_en_flux_ExB_turb_df')     
                    #     #self.i_radial_en_flux_ExB_turb_f0 = f.read('i_radial_en_flux_ExB_turb_f0')
                    #     self.i_radial_en_flux_mag_df = f.read('i_radial_en_flux_mag_df')       
                    #     self.i_radial_en_flux_mag_f0 = f.read('i_radial_en_flux_mag_f0')   
                    #     #self.i_radial_en_flux_mag_turb_df = f.read('i_radial_en_flux_mag_turb_df')  
                    #     #self.i_radial_en_flux_mag_turb_f0 = f.read('i_radial_en_flux_mag_turb_f0')
                    #     self.i_radial_flux_3db_df = f.read('i_radial_flux_3db_df')           
                    #     self.i_radial_flux_3db_f0 = f.read('i_radial_flux_3db_f0')  
                    #     #self.i_radial_flux_3db_turb_df = f.read('i_radial_flux_3db_turb_df')   
                    #     #self.i_radial_flux_3db_turb_f0 = f.read('i_radial_flux_3db_turb_f0')    
                    #     self.i_radial_flux_ExB_df = f.read('i_radial_flux_ExB_df')          
                    #     self.i_radial_flux_ExB_f0 = f.read('i_radial_flux_ExB_f0')        
                    #     #self.i_radial_flux_ExB_turb_df = f.read('i_radial_flux_ExB_turb_df')        
                    #     #self.i_radial_flux_ExB_turb_f0 = f.read('i_radial_flux_ExB_turb_f0')         
                    #     self.i_radial_flux_mag_df = f.read('i_radial_flux_mag_df')        
                    #     self.i_radial_flux_mag_f0 = f.read('i_radial_flux_mag_f0')          
                    #     #self.i_radial_flux_mag_turb_df = f.read('i_radial_flux_mag_turb_df') 
                    #     #self.i_radial_flux_mag_turb_f0 = f.read('i_radial_flux_mag_turb_f0')         
                    #     self.i_radial_pot_en_flux_3db_df = f.read('i_radial_pot_en_flux_3db_df')    
                    #     self.i_radial_pot_en_flux_3db_f0 = f.read('i_radial_pot_en_flux_3db_f0')    
                    #     #self.i_radial_pot_en_flux_3db_turb_df = f.read('i_radial_pot_en_flux_3db_turb_df')  
                    #     #self.i_radial_pot_en_flux_3db_turb_f0 = f.read('i_radial_pot_en_flux_3db_turb_f0') 
                    #     self.i_radial_pot_en_flux_ExB_df = f.read('i_radial_pot_en_flux_ExB_df')    
                    #     self.i_radial_pot_en_flux_ExB_f0 = f.read('i_radial_pot_en_flux_ExB_f0')   
                    #     #self.i_radial_pot_en_flux_ExB0_turb_df = f.read('i_radial_pot_en_flux_ExB0_turb_df') 
                    #     #self.i_radial_pot_en_flux_ExB0_turb_f0 = f.read('i_radial_pot_en_flux_ExB0_turb_f0') 
                    #     #self.i_radial_pot_en_flux_ExBt_df = f.read('i_radial_pot_en_flux_ExBt_df')  
                    #     #self.i_radial_pot_en_flux_ExBt_f0 = f.read('i_radial_pot_en_flux_ExBt_f0')   
                    #     #self.i_radial_pot_en_flux_ExBt_turb_df = f.read('i_radial_pot_en_flux_ExBt_turb_df') 
                    #     #self.i_radial_pot_en_flux_ExBt_turb_f0 = f.read('i_radial_pot_en_flux_ExBt_turb_f0') 
                    #     self.i_radial_pot_en_flux_mag_df = f.read('i_radial_pot_en_flux_mag_df')   
                    #     self.i_radial_pot_en_flux_mag_f0 = f.read('i_radial_pot_en_flux_mag_f0')    
                    #     #self.i_radial_pot_en_flux_mag_turb_df = f.read('i_radial_pot_en_flux_mag_turb_df') 
                    #     #self.i_radial_pot_en_flux_mag_turb_f0 = f.read('i_radial_pot_en_flux_mag_turb_f0')
                    #     self.i_tor_ang_mom_df = f.read('i_tor_ang_mom_df')          
                    #     self.i_tor_ang_mom_f0 = f.read('i_tor_ang_mom_f0')            
                    #     #self.i_tor_ang_mom_turb_df = f.read('i_tor_ang_mom_turb_df')             
                    #     #self.i_tor_ang_mom_turb_f0 = f.read('i_tor_ang_mom_turb_f0')         
                    #     self.i_toroidal_flow_df = f.read('i_toroidal_flow_df')           
                    #     self.i_toroidal_flow_f0 = f.read('i_toroidal_flow_f0')          
                    #     #self.i_toroidal_flow_turb_df = f.read('i_toroidal_flow_turb_df')          
                    #     #self.i_toroidal_flow_turb_f0 = f.read('i_toroidal_flow_turb_f0')

    

                    #     self.pot0 = f.read('pot0')

                        
                    #     #Scalar
                    #     # self.inode1m1 = f.read('inode1m1')
                    #     # self.iphim1 = f.read('iphim1')
                    #     # self.n_energy = f.read('n_energy')
                    #     # self.ndata = f.read('ndata')
                    #     self.nnode = f.read('nnode') #
                    #     #self.nphif3d = f.read('nphi') 
                    #     #self.step =  f.read('step') 
                    #     self.timef2d = f.read('time') #
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
        try:
            with Stream(self.xgc_path + file, 'rra') as r:
                variables_list = r.available_variables()
                for var_name in variables_list:
                    var = r.read(var_name)
                    self.array_container[var_name] = np.array(var)
            print(f"Reading {file} file sucessful.")
        except Exception as e:
            print(f"Error reading file: {e}")


    def get_loadVarxgca(self,name):
        if name in self.array_container:
            return self.array_container[str(name)]
        else:
            print(f"Variable with name '{name}' not found.")

#General FileReader Class
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
        


    

fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'

#required
#xgc1Obj = xgc1(fileDir)
#xgcaObj = xgca(fileDir)
#manager = loader(fileDir)

#Testing
# i_radial_en_flux_ExB_turb_df = xgc1Obj.get_loadVar3D('i_radial_en_flux_ExB_turb_df')
# print(i_radial_en_flux_ExB_turb_df)
data1Obj = data1(fileDir)

time = data1Obj.get_oneddiag('time')
psi = data1Obj.get_oneddiag('psi')
tindex = data1Obj.get_oneddiag('tindex')
step = data1Obj.get_oneddiag('step')

print(time)

#psi = data1Obj.get_oneddiag('psi')

#print(psi)












#psi = data1Obj.get_oneddiag('psi')
#print(psi)








# hyp_vis_rad = manager.reader('xgc.hyp_vis_rad.bp')
# grad_rz = manager.reader('xgc.grad_rz.bp')

# n_r = manager.get_loadVar('n_r')
# print(n_r)

















