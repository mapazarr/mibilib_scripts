"""Plot 2 channels of a list of FoVs.
"""
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mibidata import tiff

#GRAPH_DEBUG = 4
#GRAPH_DEBUG = 3
#GRAPH_DEBUG = 2
GRAPH_DEBUG = 1
#GRAPH_DEBUG = 0

SAVE = True
#SAVE = False

def plot_image(data, title='', ax=None, style_kwargs=None):
    """Plot image.

    Parameters
    ----------
    data : `~numpy.ndarray`
        2D image data to plot.
    title : str, optional
        Title for the plot.
    ax : `~matplotlib.axes.Axes`, optional
        Axes of the figure for the plot.
    style_kwargs : dict, optional
        Style options for the plot.

    Returns
    -------
    ax : `~matplotlib.axes.Axes`
        Axes of the figure containing the plot.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    # create plot
    fig = plt.figure()
    do_not_close_fig = False
    if ax is None:
        ax = fig.add_subplot(111)
        # if no axis object is passed by ref, the figure should remain open
        do_not_close_fig = True
    if style_kwargs is None:
        style_kwargs = dict()

    fig.set_size_inches(8., 8., forward=True)

    if not 'cmap' in style_kwargs:
        style_kwargs['cmap'] = 'afmhot'

    print(f'counts: {data.sum()}')
    # TODO: image might need some brightening method to enhance contrast

    image = ax.imshow(data,
                      origin='upper', # same as image raster order
                      interpolation='none',
                      **style_kwargs)

    # set title and axis names
    ax.set_title(title)
    #ax.set_xlabel('x / pixel')
    #ax.set_ylabel('y / pixel')

    # draw color bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(image, cax=cax, label='counts')

    # eventually close figure to avoid white canvases
    if not do_not_close_fig:
        plt.close(fig)
    return ax

def plot_1_fov(file_name, l_channel, ax=None, file_id=''):
    """Plot the channels for one FoV."""

    print()
    print(f'Plotting file: {file_name}')
    print(f' File ID: {file_id}')

    # load input
    input_folder = '~/IONpath/data/temp'
    input_folder = os.path.expanduser(input_folder) # expand home dir into string
    file_path = os.path.join(input_folder, file_name)
    image = tiff.read(file_path)

    #import IPython; IPython.embed()
    #print(f'image metadata:\n{image.metadata()}')
    #print(f'image channels:\n{image.channels}')

    # loop over channels
    for channel, axis in zip(l_channel, ax):
        # plot image
        print(f' Channel: {channel}')
        im = image[channel]
        counts = im.sum()
        #import IPython; IPython.embed()
        plot_image(im, ax=axis, title=str(file_id) + ': ' + str(channel) + ' ' + str("{:.2e}".format(counts)))
    if GRAPH_DEBUG > 3:
        plt.show() # wait until image is closed

    if GRAPH_DEBUG > 2:
        plt.show() # don't leave at the end

    return ax

###########################################################################

# get list of files to use for the plots
pd_filename_list = pd.read_csv('file_list.dat', header=None, usecols=[0], names=['Filename'])
l_file_name = pd_filename_list['Filename'].values.tolist()

# list  of channels to plot for each figure
#l_channel = [171, 172]
l_channel = [89, 113]

# define canvas with appropriate number of axes
# INFO: the amount of channels should be correlated with the number of columns
# in the ax array; also with the size of the canvas
n_files_to_plot = len(l_file_name)
n_channels_to_plot = len(l_channel)
figsize = 3 # inch
fig, ax = plt.subplots(n_files_to_plot, n_channels_to_plot,
                       figsize=(figsize*n_channels_to_plot,
                                figsize*n_files_to_plot))

# loop over files and produce the plots
count_files = 0;
for tiff_file_name in l_file_name:
    if count_files < n_files_to_plot:
        plot_1_fov(tiff_file_name, l_channel, ax[count_files], file_id=count_files)
        # TODO: define file ID in terms of the pd df index!!!
    count_files += 1

# save ouptut
if SAVE:
    output_file_name = 'plot_channels.png'
    print()
    print(f'Saving image to {output_file_name}')
    plt.savefig(output_file_name)

if GRAPH_DEBUG > 1:
    plt.show() # don't leave at the end

###########################################################################

if GRAPH_DEBUG:
    plt.show() # don't leave at the end
