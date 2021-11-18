import numpy as np
from matplotlib import pyplot as plt 
import matplotlib as mpl

def set_mpl_fonts():
	MEDIUM = 16
	SMALL = 12
	LARGE = 20
	font_params = {
	    "axes.labelsize": MEDIUM,
	    "axes.titlesize": LARGE,
	    "figure.titlesize": LARGE,
	    "font.size": MEDIUM,
	    "legend.fontsize": SMALL,
	    "legend.title_fontsize": SMALL,
	    "xtick.labelsize": SMALL,
	    "ytick.labelsize": SMALL,
	}
	for key, val in font_params.items():
	    plt.rcParams[key] = val

def set_cmap():
	min_val, max_val = 0.1, 0.8
	n = 10
	orig_cmap = plt.cm.inferno
	colors = orig_cmap(np.linspace(min_val, max_val, n))
	cmap = mpl.colors.LinearSegmentedColormap.from_list("mycmap", colors)
	return cmap
