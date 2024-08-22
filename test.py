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
fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'
handler = xgc_filereader.loader(fileDir)
xgc1Obj = xgc_filereader.xgc1(fileDir)


class meshdata(object):
    def __init__(self):
        Rmin = 2.2
        Rmax = 2.31
        Zmin = -0.25
        Zmax = 0.4
        handler.reader('/xgc.mesh.bp')
        
        

    class Core():
        def __init__(self, grid_nwall, grid_nwall_node, n_n, n_t, nd_connect_list, rz):
            self.grid_nwall = grid_nwall
            self.grid_nwall_node = grid_nwall_node
            self.n_n = n_n 
            self.n_t = n_t
            self.nd_connect_list = nd_connect_list
            self.rz = rz
            

    class Surface:
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


    class Vertex:
        def __init__(self,node_vol, node_vol_ff0, node_vol_ff1, node_vol_nearest, psi, theta):
            self.node_vol = node_vol
            self.node_vol_ff0 = node_vol_ff0
            self.node_vol_ff1 = node_vol_ff1
            self.node_vol_nearest = node_vol_nearest
            self.psi = psi
            self.theta = theta


    class Triangle:
        def __init__(self, tr_area):
            self.tr_area = tr_area

#initializing DataObj
selection = xgc1Obj.get_choice()

print(selection)
dataObj = meshdata()

#core = meshdata.Core
if selection == 1:
    print("Processing all mesh variables...")
    handler.list_Vars('/xgc.mesh.bp')
    
    try:
        
        #Core Subclass
        core = meshdata.Core(
            handler.get_loadVar('grid_nwall'),
            handler.get_loadVar('grid_nwall_node'),
            handler.get_loadVar('n_n'),
            handler.get_loadVar('n_t'),
            handler.get_loadVar('nd_connect_list'),
            handler.get_loadVar('rz')
            )
        
        
        #Surface Subclass
        surface = meshdata.Surface(
            handler.get_loadVar('epsilon'),
            handler.get_loadVar('m_max_surf'),
            handler.get_loadVar('nsurf'),
            handler.get_loadVar('psi_surf'),
            handler.get_loadVar('qsafety'),
            handler.get_loadVar('rmaj'),
            handler.get_loadVar('rmin'),
            handler.get_loadVar('surf_idx'),
            handler.get_loadVar('surf_len'),
            handler.get_loadVar('surf_maxlen'),
            handler.get_loadVar('trapped'))
            
        trangle = meshdata.Triangle(
            handler.get_loadVar('tr_area')
        )
        vertex = meshdata.Vertex(
            handler.get_loadVar('node_vol'),
            handler.get_loadVar('node_vol_ff0'),
            handler.get_loadVar('node_vol_ff1'),
            handler.get_loadVar('node_vol_nearest'),
            handler.get_loadVar('psi'),
            handler.get_loadVar('theta')
        )
        print("Data recieved from file")
        print("Performing Data Visualization...")
    except Exception as e:
        print(f"Error occured: {e}")

    print(core.grid_nwall_node)
    print(surface.nsurf)

    r = core.rz[:,0]
    z = core.rz[:,1]
    Rmin = np.min(r)
    Rmax = np.max(r)
    Zmin = np.min(z)
    Zmax = np.max(z)
    

        #setup Mesh Grid
    Ri = np.linspace(Rmin, Rmax, 400)
    Zi = np.linspace(Zmin, Zmax, 400)
    RI,ZI = np.meshgrid(Ri,Zi)

    # nd_connect_list = self.managerObj.get_loadVar('nd_connect_list')
    # grid_nwall = self.managerObj.get_loadVar('grid_nwall')
        


    triObj = Triangulation(r, z, core.nd_connect_list)

        #As = np.zeros((len(RZ[:,0]), Nplanes, Ntimes))

    dpot3D = xgc1Obj.get_loadVar3D('dpot')


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
    print("Success")


#elif user_select == 2: 
    


    






    