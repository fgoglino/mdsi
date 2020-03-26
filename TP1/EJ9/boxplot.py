# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:52:39 2020

@author: Francisco Goglino
"""
from operator import itemgetter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========
# LOAD DATA
# =========

# Load luminosity column from file estrellas.xlsx and transform to a numpy
# array for easier handling (personal preference)
luminosidad = pd.DataFrame(pd.read_excel(io="estrellas.xlsx")).to_numpy()[:,2]

# =============================
# CUSTOM BOXPLOT IMPLEMENTATION
# =============================

# Matplotlib has a standard boxplot method, but calculates quartiles in a way
# that doesn't fit those defined in class. Quartile calculation for the graph
# cannot easily be changed thus we implement our own boxplot graph using
# proper quartile calculation.

# Calculate quartiles
lum_q1 = np.quantile(luminosidad, 0.25, interpolation = "nearest")
lum_med = np.quantile(luminosidad, 0.5, interpolation = "nearest")
lum_q3 = np.quantile(luminosidad, 0.75, interpolation = "nearest")

# Calculate whiskers
lum_ric = lum_q3 - lum_q1
lum_whislo = min(val for val in luminosidad if 
                           lum_q1 - 1.5 * lum_ric <= val <= lum_q1)
lum_whishi = max(val for val in luminosidad if 
                           lum_q3 <= val <= lum_q3 + 1.5 * lum_ric)

# Generate outlier list
lum_fliers = []
gen = (val for val in luminosidad if (val < lum_whislo or val > lum_whishi))
for val in gen:
    lum_fliers.append(val)
    
# Draw the plot
fig, ax = plt.subplots()
boxes = [
    {
        'whislo': lum_whislo,    # Lower whisker
        'q1'    : lum_q1,        # Lower quartile
        'med'   : lum_med,       # Median
        'q3'    : lum_q3,        # Upper quartile
        'whishi': lum_whishi,    # Upper whisker
        'fliers': lum_fliers     # Fliers/outliers
    }
]
ax.bxp(boxes, showfliers = True) # Show fliers
plt.xticks([])                   # Remove annoying vertical major grid line
plt.minorticks_on()              # Enable grid lines
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='grey')
plt.title("Luminosidad (Relativa al Sol)")

# Save plot
plt.savefig("boxplot.png", dpi=300)
plt.close()