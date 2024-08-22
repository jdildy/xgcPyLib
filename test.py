#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.tri import Triangulation, LinearTriInterpolator
import os
from PIL import Image

import xgc_filereader
from xgc_filereader import user_select
from scipy.sparse import csr_matrix

from PIL import Image
fileDir = '/pscratch/sd/s/sku/n552pe_d3d_NT_new_profile_Jun'
handler = xgc_filereader.loader()
xgc1Obj = xgc_filereader.xgc1(fileDir)

class meshdata(object):
    def __init__(self):
        Rmin = 2.2
        Rmax = 2.31
        Zmin = -0.25
        Zmax = 0.4
        
        

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
dataObj = meshdata()

#core = meshdata.Core
if user_select == 1:
    #Core Subclass
    core = meshdata.Core(
        xgc1Obj.get_loadVar3D('grid_nwall'),
        xgc1Obj.get_loadVar3D('grid_nwall_node'),
        xgc1Obj.get_loadVar3D('n_n'),
        xgc1Obj.get_loadVar3D('n_t'),
        xgc1Obj.get_loadVar3D('nd_connect_list'),
        xgc1Obj.get_loadVar3D('rz')
        )
    
    
    #Surface Subclass
    surface = meshdata.Surface(
        xgc1Obj.get_loadVar3D('epsilon'),
        xgc1Obj.get_loadVar3D('m_max_surf'),
        xgc1Obj.get_loadVar3D('surf'),
        xgc1Obj.get_loadVar3D('psi_surf'),
        xgc1Obj.get_loadVar3D('qsafety'),
        xgc1Obj.get_loadVar3D('rmaj'),
        xgc1Obj.get_loadVar3D('rmin'),
        xgc1Obj.get_loadVar3D('surf_idx'),
        xgc1Obj.get_loadVar3D('surf_len'),
        xgc1Obj.get_loadVar3D('surf_maxlen'),
        xgc1Obj.get_loadVar3D('trapped'))
        
    trangle = meshdata.Triangle(
        xgc1Obj.get_loadVar3D('tr_area')
    )
    vertex = meshdata.Vertex(
        xgc1Obj.get_loadVar3D('node_vol'),
        xgc1Obj.get_loadVar3D('node_vol_ff0'),
        xgc1Obj.get_loadVar3D('node_vol_ff1'),
        xgc1Obj.get_loadVar3D('node_vol_nearest'),
        xgc1Obj.get_loadVar3D('psi'),
        xgc1Obj.get_loadVar3D('theta')
    )

    core.grid_nwall

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


#elif user_select == 2: 
    


    






    