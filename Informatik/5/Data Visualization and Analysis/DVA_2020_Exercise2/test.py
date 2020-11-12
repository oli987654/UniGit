import glob
import os
import numpy as np
from PIL import Image

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.layouts import layout


r = np.random.randn(100,3)
bin=(5,8,4)
H, edges = np.histogramdd(r, bins = bin)
H.shape, edges[0].size, edges[1].size, edges[2].size
((5, 8, 4), 6, 9, 5)

print(r)
print(H)
print(bin)

