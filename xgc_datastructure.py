#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.tri import Triangulation, LinearTriInterpolator
import os
from PIL import Image

import xgc_filereader
from scipy.sparse import csr_matrix

from PIL import Image

print(matplotlib.get_backend())






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
        self.managerObj.reader('/xgc.units.bp')

        self.RZ = self.managerObj.get_loadVar('rz')
        self.R=self.RZ[:,0]
        self.Z=self.RZ[:,1]

        Rmin = self.managerObj.get_loadVar('eq_x_r') if 'x' in str(Rmin).lower() else Rmin
        Rmax = self.managerObj.get_loadVar('eq_x_r') if 'x' in str(Rmax).lower() else Rmax
        Zmin = self.managerObj.get_loadVar('eq_x_z') if 'x' in str(Zmin).lower() else Zmin
        Zmax = self.managerObj.get_loadVar('eq_x_z') if 'x' in str(Zmax).lower() else Zmax

        #Nplanes = np.array(self.xgc1Obj.get_loadVar3D('dpot')).shape[1]
        mask1d = self.oned_mask()

        try:
            time = np.array(self.data1Obj.read_oneddiag('time')[mask1d],ndmin=1)
        except:
            time = [0]

        Ntimes = len(time)

        # self.managerObj.reader('/xgc.bfield.bp')
        # try:
        #     self.bfield = self.managerObj.get_loadVar('node_data[0]/values')[...]
        # except: 
        #     try:
        #         self.bfield = self.managerObj.get_loadVar('/node_data[0]/values')[...]
        #     except:
        #         self.bfield = self.managerObj.get_loadVar('bfield')[...]

        self.R= np.array(self.RZ[:,0])
        self.Z = np.array(self.RZ[:,1])
        Rmin = self.R.min
        Rmax = self.R.max
        Zmin = self.Z.min
        Zmax = self.Z.max
    

        #setup Mesh Grid
        Ri = np.linspace(Rmin, Rmax, 400)
        Zi = np.linspace(Zmin, Zmax, 400)
        RI,ZI = np.meshgrid(Ri,Zi)

        nd_connect_list = self.managerObj.get_loadVar('nd_connect_list')
        grid_nwall = self.managerObj.get_loadVar('grid_nwall')
        


        triObj = Triangulation(self.R, self.Z, nd_connect_list)

        #As = np.zeros((len(RZ[:,0]), Nplanes, Ntimes))

        dpot3D = self.xgc1Obj.get_loadVar3D('dpot')


        plt.figure(1)
        tci=LinearTriInterpolator(triObj,dpot3D[0])
        out=tci(RI,ZI)
        fac=0.25
        colra=np.arange(np.min(out)*fac,np.max(out)*fac,fac*np.abs(np.max(out)-np.min(out))*0.01)
        plt.contourf(RI,ZI,out,levels=colra)
        plt.colorbar()
        plt.xlabel('R [m]')
        plt.ylabel('Z [m]')
        plt.ion()
        # plt.savefig('mesh.png')

        # image = Image.open('mesh.png')
        plt.show()
        

    
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
            idx = np.array(idx)

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

        
            
            
#     def GradAll(self, field):
#         field = np.array(field)
#         if field.ndim!=2:
#             print("GradParX: Wrong array shape of field, must be (nnode,nphi)")
#             return -1
#         nphi  = field.shape[1]
#         nnode = field.shape[0]
#         grad_field = np.zeros((nnode,nphi,3))
#         grad_field[:,:,0:2] = self.GradPlane(field)
#         grad_field[:,:,2]   = self.GradParX(field)
#         return grad_field
    
#     def GradPlane(self,field):
#         field = np.array(field)
#         if field.ndim>2:
#             print("GradPlane: Wrong array shape of field, must be (nnode,nphi) or (nnode)")
#             return -1
#         nnode = field.shape[0]
#         if field.ndim==2:
#             field_loc = field
#             nphi = field.shape[1]
#         else:
#             nphi           = 1
#             field_loc      = np.zeros((nnode,nphi),dtype=field.dtype)
#             field_loc[:,0] = field
#         grad_field = np.zeros((nnode,nphi,2),dtype=field.dtype)
#         for iphi in range(nphi):
#             grad_field[:,iphi,0] = self.grad_mat_psi_r.dot(field_loc[:,iphi])
#             grad_field[:,iphi,1] = self.grad_mat_theta_z.dot(field_loc[:,iphi])
#         return grad_field

#     def GradParX(self, field):
#         self.managerObj.reader('/xgc.bfield.bp')
#         field = np.array(field)
#         self.managerObj.reader('/xgc.ff_1dp_fwd.bp')
#          #l_r   = self.ff_1dp_fwd_dl
#         l_r = self.managerObj.get_loadVar('dl_par')
#         self.managerObj.reader('/xgc.ff_1dp_rev.bp')
#         #l_l   = self.ff_1dp_rev_dl
#         l_l    = self.managerObj.get_loadVar('dl_par')
#         if field.ndim!=2:
#             print("GradParX: Wrong array shape of field, must be (nnode,nphi)")
#             return -1
#         nphi  = field.shape[1]
#         nnode = field.shape[0]
#         if nnode!=self.ff_1dp_fwd.shape[0]:
#             return -1
#         sgn   = np.sign(self.bfield[0,2])
#         l_tot = l_r+l_l
#         bdotgrad_field = np.zeros_like(field)
#         for iphi in range(nphi):
#             iphi_l  = iphi-1 if iphi>0 else nphi-1
#             iphi_r  = np.fmod((iphi+1),nphi)
#             field_l = self.ff_1dp_rev.dot(field[:,iphi_l])
#             field_r = self.ff_1dp_fwd.dot(field[:,iphi_r])
#             #
#             bdotgrad_field[:,iphi] = sgn * (-(    l_r)/(l_l*l_tot)*field_l        \
#                                             +(l_r-l_l)/(l_l*l_r  )*field[:,iphi]  \
#                                             +(    l_l)/(l_r*l_tot)*field_r        )
#         return bdotgrad_field


#     def load_grad_mat(self):
#         # fn = self.xgc_path+'xgc.grad_rz'
#         self.managerObj.reader('xgc_grad_rz')

#         try:
#             # Flag indicating whether gradient is (R,Z) or (psi,theta)
#             self.grad_mat_basis = self.managerObj.get_loadVar('basis')
#             # Set up matrix for psi/R derivative
#             nelement            = self.managerObj.get_loadVar('nelement_r')
#             eindex              = self.managerObj.get_loadVar('eindex_r')-1
#             value               = self.managerObj.get_loadVar('value_r')
#             nrows               = self.managerObj.get_loadVar('m_r')
#             ncols               = self.managerObj.get_loadVar('n_r')
#             self.grad_mat_psi_r = self.create_sparse_xgc(nelement,eindex,value,m=nrows,n=ncols)
#             # Set up matrix for theta/Z derivative
#             nelement              = self.managerObj.get_loadVar('nelement_z')
#             eindex                = self.managerObj.get_loadVar('eindex_z')-1
#             value                 = self.managerObj.get_loadVar('value_z')
#             nrows                 = self.managerObj.get_loadVar('m_z')
#             ncols                 = self.managerObj.get_loadVar('n_z')
#             self.grad_mat_theta_z = self.create_sparse_xgc(nelement,eindex,value,m=nrows,n=ncols)
#         except:
#             self.grad_mat_psi_r   = 0
#             self.grad_mat_theta_z = 0
#             self_grad_mat_basis   = 0

#     def create_sparse_xgc(self,nelement,eindex,value,m=None,n=None):
#     # Create Python sparse matrix from XGC data
#         nelement = np.array(nelement)
    
#         if m is None: m = nelement.size
#         if n is None: n = nelement.size
        
#         #format for Python sparse matrix
#         indptr = np.insert(np.cumsum(nelement),0,0)
#         indices = np.empty((indptr[-1],))
#         data = np.empty((indptr[-1],))
#         for i in range(nelement.size):
#                 indices[indptr[i]:indptr[i+1]] = eindex[i,0:nelement[i]]
#                 data[indptr[i]:indptr[i+1]] = value[i,0:nelement[i]]
#         #create sparse matrices
#         spmat = csr_matrix((data,indices,indptr),shape=(m,n))
#         return spmat
            
#     def conv_read2ff(self, field):
#         field = np.array(field)
#         if (field.ndim==3):
#             field_work = field
#         elif (field.ndim==2):
#             field_work = np.zeros((field.shape[0],field.shape[1],1),dtype=field.dtype)
#             field_work[:,:,0] = field[:,:]
#         else:
#             print("conv_real2ff: input field has wrong shape.")
#             return -1
#         fdim = field_work.shape[2]
#         nphi = field_work.shape[1]
#         field_ff = np.zeros((field_work.shape[0],nphi,fdim,2),dtype=field_work.dtype)
#         for iphi in range(nphi):
#             iphi_l  = iphi-1 if iphi>0 else nphi-1
#             iphi_r  = iphi
#             for j in range(fdim):
#                 field_ff[:,iphi,j,0] = self.ff_hdp_rev.dot(field_work[:,iphi_l,j])
#                 field_ff[:,iphi,j,1] = self.ff_hdp_fwd.dot(field_work[:,iphi_r,j])
#         field_ff = np.transpose(field_ff,(1,0,2,3))
#         if fdim==1:
#             field_ff = (np.transpose(field_ff,(0,1,3,2)))[:,:,:]
#         #
#         return field_ff
    
#     def load_ff_mapping(self):
#         self.ff_map_names = ["ff_1dp_fwd","ff_1dp_rev","ff_hdp_fwd","ff_hdp_rev"]
#         for ff_name in self.ff_map_names:
#             self.managerObj.reader(fileDir+'xgc.'+ff_name)
#             try:
#                 nelement = self.managerObj.get_loadVar('nelement')
#                 eindex   = self.managerObj.get_loadVar('eindex')-1
#                 value    = self.managerObj.get_loadVar('value')
#                 nrows    = self.managerObj.get_loadVar('nrows')
#                 ncols    = self.managerObj.get_loadVar('ncols')
#                 dl_par   = self.managerObj.get_loadVar('dl_par')
#                 self.__setattr__(ff_name,self.create_sparse_xgc(nelement, eindex, value, m=nrows, n=ncols))
#                 #
#                 varn     = ff_name+'_dl'
#                 self.__setattr__(varn,dl_par)
#             except:
#                 self.__setattr__(ff_name,0)


    

        




# #     #nd_connect_list -> connectivity information
# #     #rz -> 
# #     #grid_nwall
# #     #grid_nwall_nodes

   
    

    




# # # class fdata():
# # #     def __init__(self) -> None:
# # #         pass




# # # class fielddata():
# # #     def __init__(self) -> None:
# # #         pass





# # # class fluxdata():
# # #     def  __init__(self) -> None:
# # #         pass
    
 
meshdata()



    