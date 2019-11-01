import os
from dotenv import load_dotenv

import numpy as np

from mibidata import tiff, mibi_image as mi
from mibitracker.request_helpers import MibiRequests

#SAVE_OUTPUT = True
SAVE_OUTPUT = False

# get credentials and open mibi request
fname_login = '~/IONpath/MIBItracker_login.dat'
fname_login = os.path.expanduser(fname_login) # expand home dir into string
load_dotenv(fname_login)
mr = MibiRequests(os.getenv('MIBITRACKER_PUBLIC_URL'),
                  os.getenv('MIBITRACKER_PUBLIC_EMAIL'),
                  os.getenv('MIBITRACKER_PUBLIC_PASSWORD'))

# get images from mibitracker
run_name = '20180121_1250_1251'
#l_point_names = ['Point2', 'Point8']
l_point_names = ['Point2']
l_image_ids = []
for point_name in l_point_names:
    l_image_ids.append(mr.image_id(run_name, point_name))
print(f'image IDs: {l_image_ids}')
images = []
for image_id in l_image_ids:
    im = mr.get_mibi_image(image_id)
    images.append(im)
    print()
    print(f'image {image_id}')
    print(f'channels: {im.channels}')
    print(f'metadata: {im.metadata}')
    print()
    print('Adding additional metadata')
    im.optional_metadata['test'] = 'value'
    print(f'metadata: {im.metadata}')
    images.append(im)

# select first image:
print()
print('Using first image')
image = images[0]

# create an image:
new_image = mi.MibiImage(image.data, image.channels, **image.metadata())
print()
print('new image')
print(new_image)

# save a tiff
out_file_name = 'new_image.tiff'
if SAVE_OUTPUT:
    print(f'Saving image to {out_file_name}')
    tiff.write(out_file_name, new_image)

# read tiff file
new_image_from_file = tiff.read(out_file_name)
print()
print('new image from file')
print(new_image_from_file)

# compare images
assert(new_image.metadata() == new_image_from_file.metadata())
