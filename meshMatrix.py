import numpy as np
from scipy.integrate import simps


"""
Mesh Matrix class for performing essential calculations like 
Flux-Surface Average (Analyzing plasma properties over magnetic flux surfaces),
Psi-Theta Gradient (Understanding gradients in magnetic flux cooridinates),
Field-Following Projections (studies performed to understand behavior along magnetic field lines),
Gyrokinetic-Average (Simplifying particle dynamics by averaging over gyration)

Consists of 
1.) Mesh Class
    Requires:
        xgc.mesh.bp
        gc.f0.mesh.bp
2.) F - Data Class
    Requires:
        xgc.f0.xxxx.bp
3.) Field Data Class
    Requies: 
        xgc.f2d.xxxx.bp or,
        xgc.2d.xxxx.bp or,
        xgc.f3d.xxxx.bp or,
        xgc.3d.xxxx.bp
4.) Flux-Surface Averaged Data Class
    Requires: 
        xgc.oneddiag.bp

"""


class MeshMatrix: 



    def __init__(self):
        self



    