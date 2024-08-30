#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.tri import Triangulation, LinearTriInterpolator
from PIL import Image
import argparse
import os
import adios2 as ad
from scipy import  ndimage as sci
from scipy import interpolate as sp


import xgc_filereader

from PIL import Image


class mesh(object):
    def __init__(self):
        Rmin = 2.2
        Rmax = 2.31
        Zmin = -0.25
        Zmax = 0.4
        
        

    class Core():
        def __init__(self, grid_nwall, grid_wall_nodes, n_n, n_t, nd_connect_list, rz):
            self.grid_nwall = grid_nwall
            self.grid_wall_nodes = grid_wall_nodes
            self.n_n = n_n 
            self.n_t = n_t
            self.nd_connect_list = nd_connect_list
            self.rz = rz
            

    class Surface():
        def __init__(self, epsilon, m_max_surf, nsurf, psi_surf, qsafety,rmaj, rmin, surf_idx, 
                     surf_len, surf_maxlen, trapped):
            
            self.epsilon = epsilon
            self.m_max_surf = m_max_surf
            self.nsurf = nsurf
            self.psi_surf = psi_surf
            self.qsafety = qsafety
            self.rmaj = rmaj
            self.rmin = rmin
            self.surf_idx = surf_idx
            self.surf_len = surf_len
            self.surf_maxlen = surf_maxlen
            self.trapped = trapped

            

    class Vertex():
        def __init__(self,node_vol, node_vol_ff0, node_vol_ff1, node_vol_nearest, psi, theta):
            self.node_vol = node_vol
            self.node_vol_ff0 = node_vol_ff0
            self.node_vol_ff1 = node_vol_ff1
            self.node_vol_nearest = node_vol_nearest
            self.psi = psi
            self.theta = theta

    class Triangle():
        def __init__(self, tr_area):
            self.tr_area = tr_area



    # Setup for flux average and gradient matrices # 
    class matrix(object):
       
        def create_sparse_xgc(self, nelement, eindex, value, m=None, n=None):
                """
                method creates a sparse matrix for data calculation

                params np.array nelement: 1D np.array from xgc.fluxavg.
                params np.array eindex: 1D np.array from xgc.fluxavg.
                params np.array value: 2D np.array from xgc.fluxavg.

                """
                from scipy.sparse import csr_matrix
                nelement = np.array(nelement)

                if m is None: m = nelement.size
                if n is None: n = nelement.size
                

                #Creating parameters
                indptr = np.insert(np.cumsum(nelement),0,0)
                indices =np.empty((indptr[-1],))
                data = np.empty((indptr[-1],))

                for i in range(nelement.size):
                    indices[indptr[i]:indptr[i+1]] = eindex[i,0:nelement[i]]
                    data[indptr[i]:indptr[i+1]] = value[i,0:nelement[i]]
                #create sparse matrices
                spmat = csr_matrix((data,indices,indptr),shape=(m,n))
                return spmat
        

    # FluxAvg calculation class
    class FluxAvg(matrix):
        def __init__(self,fileDir):
            handler = xgc_filereader.loader(fileDir)
            try:
                handler.reader('/xgc.fluxavg.bp')
                nelement        = handler.get_loadVar('nelement')
                nelement        = np.array(nelement)
                eindex          = handler.get_loadVar('eindex')
                npsi            = handler.get_loadVar('npsi')
                value           = handler.get_loadVar('value')
                self.flux_mat   = self.create_sparse_xgc(nelement, eindex, value, m=nelement.size, n=npsi).T
                print('created flux surface average matrix sucessfully.\n')
            except:
                self.flux_mat   = 0

    # Gradient calculation class
    class Gradient(matrix):
        def __init__(self,fileDir):
            try:
                handler = xgc_filereader.loader(fileDir)
                handler.reader('/xgc.grad_rz.bp')
                self.mat_basis = handler.get_loadVar('basis')
            
                nelement = handler.get_loadVar('nelement_r')
                eindex   = handler.get_loadVar('eindex_r')-1 
                value    = handler.get_loadVar('value_r')
                nrows    = handler.get_loadVar('m_r')
                ncols    = handler.get_loadVar('n_r')
                self.grad_mat_r = self.create_sparse_xgc(nelement, eindex, value, m=nrows, n=ncols).T

                nelement = handler.get_loadVar('nelement_z')
                eindex   = handler.get_loadVar('eindex_z')-1 
                value    = handler.get_loadVar('value_z')
                nrows    = handler.get_loadVar('m_z')
                ncols    = handler.get_loadVar('n_z')
                self.grad_mat_z = self.create_sparse_xgc(nelement, eindex, value, m=nrows, n=ncols).T
                print('Created gradient matrix along r and z sucessfully.\n')
            except:
                self.grad_mat_r     = 0
                self.grad_mat_z     = 0
                self.mat_basis      = 0

    #Magenitcs Class for xgc.equil.bp data (In Progress)  
    class MagneticField():
        def __init__(self,eq_I, eq_axis_b, eq_axis_r, eq_axis_z, 
                     eq_max_r, eq_max_z, eq_min_r, eq_min_z,
                      eq_mpsi, eq_mr, eq_mz, eq_psi_grid,
                        eq_psi_rz, eq_x_psi, eq_x_r, eq_x_z):
            
            self.eq_I = eq_I
            self.eq_axis_b = eq_axis_b
            self.eq_axis_r = eq_axis_r
            self.eq_axis_z = eq_axis_z
            self.eq_max_r = eq_max_r
            self.eq_max_z = eq_max_z
            self.eq_min_r = eq_min_r
            self.eq_min_z = eq_min_z
            self.eq_mpsi = eq_mpsi
            self.eq_mr = eq_mr
            self.eq_mz = eq_mz
            self.eq_psi_grid = eq_psi_grid
            self.eq_psi_rz = eq_psi_rz
            self.eq_x_psi = eq_x_psi 
            self.eq_x_r = eq_x_r
            self.eq_x_z = eq_x_z 
            


    # HeatDiag class for xgc.heatdiag2.bp (In progress)
    class HeatDiag():
            def __init__(self,ds, e_number, e_para_energy, e_perp_energy, e_potential,
                        i_number, i_para_energy, i_perp_energy, i_potential,
                        nphi, nseg, nseg1, psi, r, strike_angle, time, z):
                self.ds = ds 
                self.e_number = e_number
                self.e_para_energy = e_para_energy
                self.e_perp_energy = e_perp_energy
                self.e_potential = e_potential

                self.i_number = i_number
                self.i_para_energy = i_para_energy
                self.i_perp_energy = i_perp_energy
                self.i_potential = i_potential
                
                self.nphi = nphi
                self.nseg = nseg 
                self.nseg1 =nseg1
                self.psi = psi
                self.r = r
                self.z = z
                self.strike_angle = strike_angle
                self.time = time

                
                
            ## PROCESS NEEDS TO BE IMPLEMENTED TO PROCESS HEATDIAG DATA ##
            # def heatdiag_proc(self):
            #     time_ht = self.time
            #     nt_ht = len(time_ht)
            #     s = len(self.r)
            #     r = self.r[:, 0]
            #     z = self.z[:, 0]
            #     psi = self.psi[:, 0]
            #     nseg = s - 1
            #     ds = np.zeros(nseg)
            #     nphi_ht = 1
            #     strike_angle = self.strike_angle[:,0]

            #     for i in range(nseg):
            #         ip = (i+1) % (nseg - 1)
            #         rm = 0.5 * (r[i]+r[ip])
            #         ds[i] = 2 * np.pi / nphi_ht * rm * np.sqrt((r[i] - r[ip])**2 + (z[i]-z[ip])**2)
                
            #     dt_ht = np.arange(nt_ht)
            #     ix_ht = np.zeros(nt_ht)


            #     for i in range(nt_ht - 1):
            #         dt_ht[i] = time_ht[i + 1] - time_ht[i]
            #     dt_ht[nt_ht-1] = dt_ht[nt_ht-2]

            #     psi_ht = psi / mesh.Surface.get_surface('psi') # I THINK THIS IS RIGHT, NOT SURE YET

            #     epload = self.e_number[:,np.arange(nt_ht)] # Check with robert if we wants to do 1: or : -> 1: selects starting from index 1(row2 instead of row 1) since python is zero-based, 
            #                                                 # : starts from the index 0 (row1)
            #     ipload = self.i_number[:,np.arange(nt_ht)]

            #     ehload = (self.e_para_energy-0 *self.e_potential * charge + self.e_perp_energy)[1:,np.arange(nt_ht)]
            #     ihload = (self.i_para_energy+0*self.i_potential * charge + self.i_perp_energy)[1:,np.arange(nt_ht)]

            #     ht_fac = np.zeros(s)
            #     s = len(epload)
            #     for i in range (s):
            #         ip = i % (s - 2)
            #         ht_fac[i] = ds[ip] * np.cos(strike_angle[i])

            #     nl_ht = len(ipload[:,0,0])
            #     len_ht = np.zeros(nl_ht)
            #     rm = np.zeros(nl_ht)
            #     zm = np.zeros(nl_ht)

            #     for i in range(1, nl_ht):
            #         len_ht[i] = len_ht[i-1] + np.sqrt((rm[i]-rm[i - 1])**2 + (zm[i]-zm[i - 1])**2)
                
            #     # Ensure psi, r, z, and length are in counter-clockwise direction
            #     psi_ht_r = psi_ht
            #     r_ht_r = r
            #     z_ht_r = z
            #     len_ht_r = len_ht

            #     # Interpolate psi and length to limited sections of the inner and outer
            #     # Divertor for plotting the results

            #     ht_res = 501
            #     l0  = len_ht_r[np.argmin(psi_ht_r)]
            #     # Outer Divertor
            #     ix_out = np.where((psi_ht_r >= 0.97) & (psi_ht_r <= 1.12) & (len_ht_r >= l0) & (z_ht_r < -0.5))
            #     len_ht_out = np.linspace(min(len_ht_r[ix_out]), max(len_ht_r[ix_out]), ht_res)
            #     r_interp = sp.interp1d(r_ht_r[ix_out],len_ht_r[ix_out])
            #     r_ht_out = r_interp(len_ht_out)
            #     z_interp = sp.interp1d(z_ht_r[ix_out],len_ht_r[ix_out])
            #     z_ht_out = z_interp(len_ht_out)


            #     # Inner Divertor
            #     ix_in= np.where((psi_ht_r >= 0.97) & (psi_ht_r <= 1.12) & (len_ht_r <= l0) & (z_ht_r < -0.5))
            #     len_ht_in = np.linspace(max(len_ht_r[ix_in]), min(len_ht_r[ix_in]), ht_res)
            #     r_interp = sp.interp1d(len_ht_r[ix_in],r_ht_r[ix_in])
            #     r_ht_in = r_interp(len_ht_in)
            #     z_interp = sp.interp1d(len_ht_r[ix_in],r_ht_r[ix_in])
            #     z_ht_in = z_interp(len_ht_in)

            #     psi_ht_out_interp = sp.interp1d(psi_ht_r[:,0],len_ht_r)
            #     psi_ht_out = psi_ht_out_interp(len_ht_out)

            #     psi_ht_in_interp = sp.interp1d(psi_ht_r[:,0], len_ht_r)
            #     psi_ht_in = psi_ht_in_interp(len_ht_in)

            #     # Generating Midplane Missing #
                
            #     # xgc_2d_2_line,mesh,mesh.psi,0,mesh.rmaxis,mesh.zmaxis,0,rl,zl,pl,pl2,res_fac=3
            #     # i0=(where(abs(rl-mesh.rmaxis) eq min(abs(rl-mesh.rmaxis))))(0)
            #     # i1=(where(pl(i0:) eq max(pl(i0:*)))+i0)(0)
            #     # im1=(where(pl(0:i0) eq max(pl(0:i0))))(0)
            #     # r0_out=interpol(rl(i0:i1),pl(i0:i1),1d0)
            #     # r0_in =interpol(rl(im1:i0),pl(im1:i0),1d0)
            #     # r_mid_ht_out= interpol(rl(i0:i1) ,pl(i0:i1) ,psi_ht_out)-r0_out
            #     # r_mid_ht_in =-interpol(rl(im1:i0),pl(im1:i0),psi_ht_in )+r0_in

            #     # Calculate Heat Load
            #     epload = np.array(epload)
            #     ipload = np.array(ipload)
            #     s = ipload.size
            #     div_loads_raw = np.zeros((s[0],s[1],4), dtype=np.float64)
            #     div_loads_raw[:,:,0] = ipload
            #     div_loads_raw[:,:,1] = epload
            #     div_loads_raw[:,:,2] = ihload
            #     div_loads_raw[:,:,3] = ehload
            #     div_loads_raw_bak = div_loads_raw

            #     kernel = [0,4,0]

            #     # div_loads_raw_smooth = sp.gaussian_filter1d(div_loads_raw_bak,)
                

            #     for k in range(4): 
            #         for it in range(nl_ht):
            #             div_loads_raw[:,it,k] /= dt_ht

            #     for i in range(nt_ht): 
            #         div_loads_raw[:,i,:] /= dt_ht[i]

            #     ht_avg = 2
            #     div_loads_r = div_loads_raw
            #     div_loads_mean_out = np.zeros(ht_res, s[1] // 2, 4)
            #     div_loads_mean_in = div_loads_mean_out

            #     # Outer divertor
            #     for isig in range(4):
            #         dum = np.zeros((ht_res,s[1]))
            #         for i in range(s[1]):
            #             dum_interp = sp.interp1d(div_loads_r[:,i,isig], len_ht_r)
            #             dum[:,i] = dum_interp(len_ht_out)
            #         for i in s[1]/ht_avg - 1:
            #             for k in ht_res - 1:
            #                 div_loads_mean_out[k,i,isig] = np.mean(dum[k,i*ht_avg:(i+1)*ht_avg])

            #     # Inner divertor 
            #     for isig in range(4):
            #         dum = np.zeros((ht_res,s[1]))
            #         for i in range(s[1]):
            #             dum_interp = sp.interp1d(div_loads_r[:,i,isig], len_ht_r)
            #             dum[:,i] = dum_interp(len_ht_in)
            #         for i in s[1]/ht_avg - 1:
            #             for k in ht_res - 1:
            #                 div_loads_mean_out[k,i,isig] = np.mean(dum[k,i*ht_avg:(i+1)*ht_avg])

            #     mhload_out1 = div_loads_mean_out[:,:,2] + div_loads_mean_out[:,:,3]
            #     mhload_in1 = div_loads_mean_in[:,:,2] + div_loads_mean_in[:,:,3]

            #     i_in  = np.min(np.where(r_mid_ht_out >= -2e-3))
            #     i_out = np.min(np.where(r_mid_ht_out >=  2e-2))

            #     eich_param_out1=[2e7,1e6,1e-3,1e-3,1e-3]
            #    # gsmooth,mhload_out1[:,itx_f3d(1)/ht_avg],fit_in,20,15
            #    # eichfit_out1=curvefit(r_mid_ht_out(i_in:i_out),fit_in(i_in:i_out),weights,eich_param_out1,function_name='eich_func2',itmax=10000,tol=1e-8)
                
            #     eich_param_out2=[2e7,1e6,1e-3,1e-3,1e-3]
            #    # gsmooth,mhload_out1(*,itx_f3d(1)/ht_avg),fit_in,20,15
            #    # eichfit_out2=curvefit(r_mid_ht_out(i_in:i_out),fit_in(i_in:i_out),weights,eich_param_out2,function_name='eich_func2',itmax=10000,tol=1e-8)

            #     # Total heat load:
            #     mhload_out_tot = np.zeros(nt_ht/ht_avg)
            #     mhload_in_tot = np.zeros(nt_ht/ht_avg)
            #     #l0_in =interpol(len_ht_in ,psi_ht_in ,1)
            #     #l0_out=interpol(len_ht_out,psi_ht_out,1)
            #     #sa_out = interpol((strike_angle[:,0]),len_ht_r,len_ht_out)
            #     #sa_in  = interpol((strike_angle[:,0]),len_ht_r,len_ht_in )
            #     #for i in range(nt_ht//ht_avg):
            #         #mhload_out_tot[i] = int_tabulated(len_ht_out-l0_out,r_ht_out*mhload_out1[:,i]*np.cos(sa_out))
            #     #for i in range(nt_ht//ht_avg):
            #         #mhload_in_tot[i]= int_tabulated(l0_in-len_ht_in  ,r_ht_in*mhload_in1 [:,i]*np.cos(sa_in))
            #     four_pi = 4 * np.pi
            #     mhload_out_tot*=four_pi
            #     mhload_in_tot *=four_pi
            #     mhload_tot=mhload_in_tot+mhload_out_tot

            #     ehload_tot=np.zeros(nt_ht) 
            #     for i in range(nt_ht):
            #         ehload_tot[i]=np.sum(ehload[:,i])/dt_ht[i]
            #     ihload_tot=np.zeros(nt_ht)
            #     for i in range(nt_ht):
            #         ihload_tot[i]=np.sum(ihload[:,i])/dt_ht(i)
            #     hload_tot=ihload_tot+ehload_tot



            # def smooth(load, kernel): 
            #     smooth = np.zeros_like(load)
            #     load = np.array(load)

            #     for i in range(load.shape[2]):
            #         smooth[:,:,i] = sci.convolve(load[:,:,i], kernel[:, np.newaxis])






                








    

#Example Case Ignore lines with ##

# #initializing DataObj
## selection = xgc1Obj.get_choice()

# gradient = Gradient()
# fluxavg = FluxAvg()

# dataObj = meshdata()

## if selection == 1:
##     print("Processing all mesh variables...")
    
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

## elif selection == 2: 

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

## else:
##     print("End")


    




    






    