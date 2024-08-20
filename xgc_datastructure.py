#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation, LinearTriInterpolator
import os
import xgc_filereader



fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'

class meshdata():
    
    #managerObj = xgc_filereader.loader(fileDir)
    # managerObj.reader('/xgc.mesh.bp')

    # nodes = managerObj.get_loadVar('nd_connect_list')
    # print(nodes)
    # RZ = managerObj.get_loadVar('rz')
    # print(RZ)
    managerObj = xgc_filereader.loader(fileDir)

    managerObj.reader('/xgc.mesh.bp')

    # rz = manager.get_loadVar('rz')
    # print(rz)


    




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