#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation, LinearTriInterpolator
import os
import xgc_filereader

class meshdata():
    fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'
    managerObj = xgc_filereader.loader(fileDir)
    managerObj.reader('/xgc.mesh.bp')

    nodes = managerObj.get_loadVar('nd_connect_list')
    RZ = managerObj.get_loadVar('rz')




    




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