#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.tri import Triangulation, LinearTriInterpolator
from PIL import Image
import argparse
import os
import adios2 as ad


import xgc_filereader

from PIL import Image
  

# parser = argparse.ArgumentParser(description='Get a directory path through command line input.')

# parser.add_argument('--input', type=str, help='Requires the rundir that holds all xgc data.')
# args = parser.parse_args()
# fileDir = args.input

       
#fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'


try:
    fileDir = xgc_filereader.checkpath('/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun')
except ValueError as e:
    print(f"Error:{e}")

oneddiag = xgc_filereader.data1(fileDir)

print(oneddiag.read_oneddiag('cden00_1d').ndim)



# handler = xgc_filereader.loader(fileDir)
# xgcaObj = xgc_filereader.xgca(fileDir)
# xgc1Obj = xgc_filereader.xgc1(fileDir)



# class meshdata(object):
#     def __init__(self):
#         Rmin = 2.2
#         Rmax = 2.31
#         Zmin = -0.25
#         Zmax = 0.4
#         handler.reader('/xgc.mesh.bp')
        
        

#     class Core():
#         def __init__(self, grid_nwall, grid_wall_nodes, n_n, n_t, nd_connect_list, rz):
#             self.grid_nwall = grid_nwall
#             self.grid_wall_nodes = grid_wall_nodes
#             self.n_n = n_n 
#             self.n_t = n_t
#             self.nd_connect_list = nd_connect_list
#             self.rz = rz          

#     class Surface():
#         def __init__(self, epsilon, m_max_surf, nsurf, psi_surf, qsafety,rmaj, rmin, surf_idx, 
#                      surf_len, surf_maxlen, trapped):
            
#             self.epsilon = epsilon
#             self.m_max_surf = m_max_surf
#             self.nsurf = nsurf
#             self.psi_surf = psi_surf
#             self.qsafety = qsafety
#             self.rmaj = rmaj
#             self.rmin = rmin
#             self.surf_idx = surf_idx
#             self.surf_len = surf_len
#             self.surf_maxlen = surf_maxlen
#             self.trapped = trapped

#     class Vertex():
#         def __init__(self,node_vol, node_vol_ff0, node_vol_ff1, node_vol_nearest, psi, theta):
#             self.node_vol = node_vol
#             self.node_vol_ff0 = node_vol_ff0
#             self.node_vol_ff1 = node_vol_ff1
#             self.node_vol_nearest = node_vol_nearest
#             self.psi = psi
#             self.theta = theta

#     class Triangle():
#         def __init__(self, tr_area):
#             self.tr_area = tr_area


# # Setup for flux average and gradient matrices # 
# class matrix(object):
#      def create_sparse_xgc(self, nelement, eindex, value, m=None, n=None):
#             from scipy.sparse import csr_matrix
#             nelement = np.array(nelement)

#             if m is None: m = nelement.size
#             if n is None: n = nelement.size
            

#             #Creating parameters
#             indptr = np.insert(np.cumsum(nelement),0,0)
#             indices =np.empty((indptr[-1],))
#             data = np.empty((indptr[-1],))

#             for i in range(nelement.size):
#                 indices[indptr[i]:indptr[i+1]] = eindex[i,0:nelement[i]]
#                 data[indptr[i]:indptr[i+1]] = value[i,0:nelement[i]]
#             #create sparse matrices
#             spmat = csr_matrix((data,indices,indptr),shape=(m,n))
#             return spmat
     


# class FluxAvg(matrix):
#     def __init__(self):
#         try:
#             handler.reader('/xgc.fluxavg.bp')
#             nelement        = handler.get_loadVar('nelement')
#             nelement        = np.array(nelement)
#             eindex          = handler.get_loadVar('eindex')
#             npsi            = handler.get_loadVar('npsi')
#             value           = handler.get_loadVar('value')
#             self.flux_mat   = self.create_sparse_xgc(nelement, eindex, value, m=nelement.size, n=npsi).T
#             print('created flux surface average matrix sucessfully.\n')
#         except:
#             self.flux_mat   = 0


# class Gradient(matrix):
#     def __init__(self):
#         try:
#             handler.reader('/xgc.grad_rz.bp')
#             self.mat_basis = handler.get_loadVar('basis')
        
#             nelement = handler.get_loadVar('nelement_r')
#             eindex   = handler.get_loadVar('eindex_r')-1 
#             value    = handler.get_loadVar('value_r')
#             nrows    = handler.get_loadVar('m_r')
#             ncols    = handler.get_loadVar('n_r')
#             self.grad_mat_r = self.create_sparse_xgc(nelement, eindex, value, m=nrows, n=ncols).T

#             nelement = handler.get_loadVar('nelement_z')
#             eindex   = handler.get_loadVar('eindex_z')-1 
#             value    = handler.get_loadVar('value_z')
#             nrows    = handler.get_loadVar(('m_z'))
#             ncols    = handler.get_loadVar('n_z')
#             self.grad_mat_z = self.create_sparse_xgc(nelement, eindex, value, m=nrows, n=ncols).T
#             print('Created gradient matrix along r and z sucessfully.\n')
#         except:
#             self.grad_mat_r     = 0
#             self.grad_mat_z     = 0
#             self.mat_basis      = 0

            



# class HeatDiag():
#         def __init__(self,ds, e_number, e_para_energy, e_perp_energy, e_potential,
#                      i_number, i_para_energy, i_perp_energy, i_potential,
#                      nphi, nseg, nseg1, psi, r, strike_angle, time, z)
#             self.ds = ds 
#             self.e_number = e_number
#             self.e_para_energy = e_para_energy
#             self.e_perp_energy = e_perp_energy
#             self.e_potential = e_potential

#             self.i_number = i_number
#             self.i_para_energy = i_para_energy
#             self.i_perp_energy = i_perp_energy
#             self.i_potential = i_potential
            
#             self.nphi = nphi
#             self.nseg = nseg 
#             self.nseg1 =nseg1
#             self.psi = psi
#             self.r = r
#             self.strike_angle = strike_angle
#             self.time = time
#             self.z = z


#             time_ht = self.time
#             nt_ht = len(self.time)


# HeatDiag()
    



# #initializing DataObj
# selection = xgc1Obj.get_choice()

# gradient = Gradient()
# fluxavg = FluxAvg()

# dataObj = meshdata()

# if selection == 1:
#     print("Processing all mesh variables...")
    
#     try:
#         #Core Subclass
#         core = meshdata.Core(
#             handler.get_loadVar('grid_nwall'),
#             handler.get_loadVar('grid_wall_nodes'),
#             handler.get_loadVar('n_n'),
#             handler.get_loadVar('n_t'),
#             handler.get_loadVar('nd_connect_list'),
#             handler.get_loadVar('rz')
#             )
        
        
#         #Surface Subclass
#         surface = meshdata.Surface(
#             handler.get_loadVar('epsilon'),
#             handler.get_loadVar('m_max_surf'),
#             handler.get_loadVar('nsurf'),
#             handler.get_loadVar('psi_surf'),
#             handler.get_loadVar('qsafety'),
#             handler.get_loadVar('rmaj'),
#             handler.get_loadVar('rmin'),
#             handler.get_loadVar('surf_idx'),
#             handler.get_loadVar('surf_len'),
#             handler.get_loadVar('surf_maxlen'),
#             handler.get_loadVar('trapped'))
            
#         trangle = meshdata.Triangle(
#             handler.get_loadVar('tr_area')
#         )
#         vertex = meshdata.Vertex(
#             handler.get_loadVar('node_vol'),
#             handler.get_loadVar('node_vol_ff0'),
#             handler.get_loadVar('node_vol_ff1'),
#             handler.get_loadVar('node_vol_nearest'),
#             handler.get_loadVar('psi'),
#             handler.get_loadVar('theta')
#         )
#         print("Data recieved from file")
#         print("Performing Data Visualization...")

#     except Exception as e:
#         print(f"Error occured: {e}")


#     r = core.rz[:,0]
#     z = core.rz[:,1]
#     Rmin = np.min(r)
#     Rmax = np.max(r)
#     Zmin = np.min(z)
#     Zmax = np.max(z)
    

#         #setup Mesh Grid
#     Ri = np.linspace(Rmin, Rmax, 400)
#     Zi = np.linspace(Zmin, Zmax, 400)
#     RI,ZI = np.meshgrid(Ri,Zi)

#     # nd_connect_list = self.managerObj.get_loadVar('nd_connect_list')
#     # grid_nwall = self.managerObj.get_loadVar('grid_nwall')
        


#     triObj = Triangulation(r, z, core.nd_connect_list)

#         #As = np.zeros((len(RZ[:,0]), Nplanes, Ntimes))

#     dpot3D = xgc1Obj.get_loadVar3D('dpot')
#     dpotF3D = xgc1Obj.get_loadVarF3D('dpot')
#     # print(len(dpotF3D[1])) 16
#     # print(len(dpotF3D[0])) 16
#     # print(len(r)) 132273
#     # print(len(z)) 132273
#     # print(len(dpot3D[0])) 132273
    

    

#     plt.figure(1)
#     tci=LinearTriInterpolator(triObj,dpot3D[0])
#     out=tci(RI,ZI)
#     fac=0.25
#     colra=np.arange(np.min(out)*fac,np.max(out)*fac,fac*np.abs(np.max(out)-np.min(out))*0.01)
#     plt.contourf(RI,ZI,out,levels=colra)
#     plt.colorbar()
#     plt.xlabel('R [m]')
#     plt.ylabel('Z [m]')
#     #plt.ion()
#     plt.show()
#     print("Success")

# elif selection == 2: 

#     start, end, step = xgc1Obj.get_timesteps()

#     # Convert into int for iterations
#     start = int(start)
#     end = int(end)
#     step = int(step)

#     data3D = xgc1Obj.get_mult3Data()
#     result = []

#     for var in data3D:
#         if 'dpot' in var:
#             result.append({'dpot': var['dpot']})

# else:
#     print("End")


    




    






    