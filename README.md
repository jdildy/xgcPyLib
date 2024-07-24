This will serve as the new data analysis library for XGC
Basic Functionality
  * Query function for listing available diagnostic output and time slices
  * Reader functions for 1D and 2D/3D data, mesh files, equilibrium, etc.
  * Mesh data structure
    - What’s the best way to encapsulate this? Analogous to the implementation in XGC, i.e., grid class, plane class, grid/plane field class? Or should 2D/3D data just be read as Numpy arrays and the mesh is a separate class that contains functions that can act upon those arrays?
  * Mesh matrix class for, e.g., flux-surface average, psi-theta gradient, field-following projections, gyro-average etc.
    - And corresponding routines for matrix multiplication and projection (in Robert’s fork of python_xgc)
  * F distribution function reader - xgc.f0.xxx.bp
  * Basic visualization routines for:
  * Installation instructions, e.g. a requirements.txt file with the required python packages which can then be installed with pip install -r requirements.txt
  * More Coming Soon!

Data Analysis Functionality 
  * Calculate neoclassical and turbulent (ExB + dB) radial flux densities (particles, momentum, heat)
  * Process “fsourcediag” and produce useful quantities (e.g. neutral fueling rate, local heating power, etc.)
  * Process wall particle/heat load diagnostic to produce useful quantities (heat load footprint, Eich-fit, 3D load patterns,...)
  * Particle and power balance diagnostic
    - Involves divergence of radial fluxes, fueling/heating, wall losses, radiation losses
  * Fourier analysis of 3D data
  * Maybe performance output, too?
  * Some utility functions that can handle XGC input files
    - SK has some routines that can read/adjust/visualize profile data file, g-eqdsk, eqd files.

