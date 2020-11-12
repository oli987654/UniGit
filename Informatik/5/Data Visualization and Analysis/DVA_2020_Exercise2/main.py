import glob
import os
import numpy as np
from PIL import Image

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.layouts import layout

# Dependencies
# Make sure to install the additional dependencies noted in the requirements.txt using the following command:
# pip install -r requirements.txt

# You might want to implement a helper function for the update function below or you can do all the calculations in the
# update callback function.

# Only do this once you've followed the rest of the instructions below and you actually reach the part where you have to
# configure the callback of the lasso select tool. The ColumnDataSource containing the data from the dimensionality
# reduction has an on_change callback routine that is triggered when certain parts of it are selected with the lasso
# tool. More specifically, a ColumnDataSource has a property named selected, which has an on_change routine that can be
# set to react to its "indices" attribute and will call a user defined callback function. Connect the on_change routine
# to the "indices" attribute and an update function you implement here. (This is similar to the last exercise but this
# time we use the on_change function of the "selected" attribute of the ColumnDataSource instead of the on_change
# function of the select widget).
# In simpler terms, each time you select a subset of image glyphs with the lasso tool, you want to adjust the source
# of the channel histogram plot based on this selection.
# Useful information:
# https://docs.bokeh.org/en/latest/docs/reference/models/sources.html
# https://docs.bokeh.org/en/latest/docs/reference/models/tools.html
# https://docs.bokeh.org/en/latest/docs/reference/models/selections.html#bokeh.models.selections.Selection


# Fetch the number of images using glob or some other path analyzer
N = len(glob.glob("static/*.jpg"))


# Find the root directory of your app to generate the image URL for the bokeh server
ROOT = os.path.split(os.path.abspath("."))[1] + "/"


# Number of bins per color for the 3D color histograms
N_BINS_COLOR = 16
# Number of bins per channel for the channel histograms
N_BINS_CHANNEL = 50
N_BINS=[]
x=255/50
y=0
while y<N_BINS_CHANNEL:
    N_BINS.append(y*x)
    y+=1


# Define an array containing the 3D color histograms. We have one histogram per image each having N_BINS_COLOR^3 bins.
# i.e. an N * N_BINS_COLOR^3 array
color_histograms=[]


# Define an array containing the channel histograms, there is one per image each having 3 channel and N_BINS_CHANNEL
# bins i.e an N x 3 x N_BINS_CHANNEL array
channel_histograms=[]

# initialize an empty list for the image file paths
filepaths=[]


# Compute the color and channel histograms
for idx, f in enumerate(glob.glob("static/*.jpg")):
    # open image using PILs Image package
    im=Image.open(f)
    # Convert the image into a numpy array and reshape it such that we have an array with the dimensions (N_Pixel, 3)
    im_array=np.asarray(im)
    
    temp=[]
    for x in im_array:
        for y in x:
            temp.append(y)
    
    im_array=np.asarray(temp)
    

    

    # Compute a multi dimensional histogram for the pixels, which returns a cube
    # reference: https://numpy.org/doc/stable/reference/generated/numpy.histogramdd.html
    h=np.histogramdd(im_array,bins=N_BINS_COLOR)


    # However, later used methods do not accept multi dimensional arrays, so reshape it to only have columns and rows
    # (N_Images, N_BINS^3) and add it to the color_histograms array you defined earlier
    # reference: https://numpy.org/doc/stable/reference/generated/numpy.reshape.html
    new_h=np.reshape(im_array,-1)
    color_histograms.append(new_h)


    # Append the image url to the list for the server
    url = ROOT + f
    filepaths.append(url)

    # Compute a "normal" histogram for each color channel (rgb)
    # reference: https://numpy.org/doc/stable/reference/generated/numpy.histogram.html
    red=[]
    green=[]
    blue=[]
    for x in im_array:
        red.append(x[0])
        green.append(x[1])
        blue.append(x[2])
    
    red=np.asarray(red)
    green=np.asarray(green)
    blue=np.asarray(blue)

    temp=[]
    temp.append(np.histogram(red,bins=N_BINS))
    temp.append(np.histogram(green,bins=N_BINS))
    temp.append(np.histogram(blue,bins=N_BINS))

    
    # and add them to the channel_histograms
    channel_histograms.append(temp)



# Calculate the indicated dimensionality reductions
# references:
# https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
# https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

# Construct a data source containing the dimensional reduction result for both the t-SNE and the PCA and the image paths

v=[]
for x in channel_histograms:
    w=[]
    sum=0
    t=0
    value=0.0
    for y in x[0][0]:
        sum=sum+y
        value=value+y*x[0][1][t]
        t+=1
    w.append(value/sum)
    
    sum=0
    t=0
    value=0.0
    for y in x[1][0]:
        sum=sum+y
        value=value+y*x[1][1][t]
        t+=1
    w.append(value/sum)

    sum=0
    t=0
    value=0.0
    for y in x[2][0]:
        sum=sum+y
        value=value+y*x[2][1][t]
        t+=1

    w.append(value/sum)

    v.append(w)

#print(v) 

Embedded=TSNE(n_components=3).fit_transform(v)

print(len(Embedded))




# Create a first figure for the t-SNE data. Add the lasso_select, wheel_zoom, pan and reset tools to it.



# And use bokehs image_url to plot the images as glyphs
# reference: https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/image_url.html

# Since the lasso tool isn't working with the image_url glyph you have to add a second renderer (for example a circle
# glyph) and set it to be completely transparent. If you use the same source for this renderer and the image_url,
# the selection will also be reflected in the image_url source and the circle plot will be completely invisible.


# Create a second plot for the PCA result. As before, you need a second glyph renderer for the lasso tool.
# Add the same tools as in figure 1

# Construct a datasource containing the channel histogram data. Default value should be the selection of all images.
# Think about how you aggregate the histogram data of all images to construct this data source

# Construct a histogram plot with three lines.
# First define a figure and then make three line plots on it, one for each color channel.
# Add the wheel_zoom, pan and reset tools to it.

# Connect the on_change routine of the selected attribute of the dimensionality reduction ColumnDataSource with a
# callback/update function to recompute the channel histogram. Also read the topmost comment for more information.

# Construct a layout and use curdoc() to add it to your document.


# You can use the command below in the folder of your python file to start a bokeh directory app.
# Be aware that your python file must be named main.py and that your images have to be in a subfolder name "static"

# bokeh serve --show .
# python -m bokeh serve --show .

# dev option:
# bokeh serve --dev --show .
# python -m bokeh serve --dev --show .