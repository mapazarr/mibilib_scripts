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
    #im.optional_metadata['test'] = 'value'
    im.test0 = 'value'
    im.test1 = 'value'
    im.test2 = 'value'
    im.test3 = 'value'
    im.test4 = 'value'
    im.test5 = 'value'
    im.test6 = 'value'
    im.test7 = 'value'
    im.test8 = 'value'
    im.test9 = 'value'
    #print(f'metadata: {im.metadata}')
    print(f'metadata: {im.metadata()}')
    images.append(im)

# select first image:
print()
print('Using first image')
image = images[0]

# access optional metadata
#print()
#print(f'optional_metadata: {image.optional_metadata}')
#print(f"test: {image.optional_metadata['test']}")
#for k, v in image.optional_metadata.items():
#    print(f'{k}: {v}')

# set additional metadata
image.test_out = 'value_out'
print()
print(f'image.test_out: {image.test_out}')

# print names of all attributes in object
print()
print(im.__dict__.keys())

#import IPython; IPython.embed()

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
print(new_image.metadata())
print(new_image_from_file.metadata())
assert(new_image.metadata() == new_image_from_file.metadata())

print()
print('Done.')
