#import xgc_filereader as r
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation, LinearTriInterpolator
import os
import xgc_filereader
from scipy.sparse import csr_matrix

import numpy as np





# Step 1: Generate Sample Data
x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
y = np.sin(x)  # y is the sine of x

# Step 2: Create the Plot
plt.figure(figsize=(8, 6))  # Set the size of the figure

plt.plot(x, y, color='b', linestyle='-', marker='o', markersize=5)  # Plot the data

# Step 3: Add Labels and Title
plt.xlabel('X axis')  # Label for the x-axis
plt.ylabel('Y axis')  # Label for the y-axis
plt.title('Simple Line Plot')  # Title of the plot

# Add grid for better readability
plt.grid(True)

# Step 4: Display the Plot
plt.show()

