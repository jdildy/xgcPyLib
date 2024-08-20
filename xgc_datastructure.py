#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation, LinearTriInterpolator
import os
import xgc_filereader



fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'

class meshdata(object):
    

    def __init__(self):
        Rmin = 2.2
        Rmax = 2.31
        Zmin = -0.25
        Zmax = 0.4


        self.managerObj = xgc_filereader.loader(fileDir)
        # xgc1 object
        self.xgc1Obj = xgc_filereader.xgc1(fileDir)
        # oneddiag object
        self.data1Obj =  xgc_filereader.data1(fileDir)
        

        self.managerObj.reader('/xgc.mesh.bp')
        self.managerObj.reader('xgc.units.bp')

        RZ = self.managerObj.get_loadVar('rz')
    
        R = RZ[:,0]
        Z = RZ[:,1]

        Rmin = self.managerObj.get_loadVar('eq_x_r') if 'x' in str(Rmin).lower() else Rmin
        Rmax = self.managerObj.get_loadVar('eq_x_r') if 'x' in str(Rmax).lower() else Rmax
        Zmin = self.managerObj.get_loadVar('eq_x_z') if 'x' in str(Zmin).lower() else Zmin
        Zmax = self.managerObj.get_loadVar('eq_x_z') if 'x' in str(Zmax).lower() else Zmax

        Nplanes = np.array(self.xgc1Obj.get_loadVar3D('dpot')).shape[1]
        mask1d = self.oned_mask()

        try:
            time = np.array(self.data1Obj.read_oneddiag('time')[mask1d],ndmin=1)
        except:
            time = [0]

        Ntimes = len(time)

        print(time)
        
        

    

    #setup Mesh Grid
        Ri = np.linspace(Rmin, Rmax, 400)
        Zi = np.linspace(Zmin, Zmax, 400)
        RI,ZI = np.meshgrid(Ri,Zi)

        nd_connect_list = self.managerObj.get_loadVar('nd_connect_list')

        triObj = Triangulation(R, Z, nd_connect_list)

        As = np.zeros((len(RZ[:,0]), Nplanes, Ntimes))

        # print(type(As))
        # print(As)

    
    
  
    
        
        #managerObj = xgc_filereader.loader(fileDir)
        # managerObj.reader('/xgc.mesh.bp')

        # nodes = managerObj.get_loadVar('nd_connect_list')
        # print(nodes)
        # RZ = managerObj.get_loadVar('rz')
        # print(RZ)

    

    def oned_mask(self):
        try:
            step = self.data1Obj.read_oneddiag('step')
            dstep = step[1] - step[0]

            idx = np.arange(step[0]/dstep[-1]/dstep+1)

            mask1d = np.zeros(idx.shape, dtype=np.int32)
            for(i,idxi) in enumerate(idx):
                mask1d[i] = np.where(step == idxi*dstep)[0][-1]
        except:
            mask1d = Ellipsis

        return mask1d
        #general reader object
    
        # Calculate grad(As) and transfrom As and grad(As)
        # to field-following representation


        #dAs = GradAll()

        #tci = LinearTriInterpolator(triObj,As_phi_ff[])
        #out=tci

        
            
            
        #def GradAll(field):

            
        #def conv_read2ff():



        
        


        




#     #nd_connect_list -> connectivity information
#     #rz -> 
#     #grid_nwall
#     #grid_nwall_nodes

#     x = [1, 2, 3, 4, 5]
#     y = [2, 3, 5, 7, 11]

#     # Create a new figure
#     plt.figure()

#     # Plot the data
#     plt.plot(x, y, marker='o', linestyle='-', color='b')

#     # Add a title and labels
#     plt.title('Simple Line Plot')
#     plt.xlabel('X-axis')
#     plt.ylabel('Y-axis')

#     # Display the plot
#     plt.show()

#     triObj = Triangulation()


    

    




# # class fdata():
# #     def __init__(self) -> None:
# #         pass




# # class fielddata():
# #     def __init__(self) -> None:
# #         pass





# # class fluxdata():
# #     def  __init__(self) -> None:
# #         pass
    
meshdata()



    