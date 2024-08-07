import numpy as np
import xgc
from matplotlib.tri import Triangulation, LinearTriInterpolator

import matplotlib.pyplot as plt

Rmin = 2.2
Rmax = 2.31
Zmin = -0.25
Zmax = 0.4

phi_start = 0
phi_end = 1
t_start = 1
t_end = 2

fileDir = '/pscratch/sd/j/jdildy/XGC-Devel/project_dir/rundir/'


loader=xgc.load(fileDir,Rmin=Rmin,Rmax=Rmax,Zmin=Zmin,Zmax=Zmax,phi_start=phi_start,phi_end=phi_end)


plt.figure(1)
plt.triplot(loader.RZ[:,0],loader.RZ[:,1],loader.tri)
