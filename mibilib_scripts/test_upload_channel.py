"""Test uploading a mibiimage to mibitracker."""

import os
import io
from skimage import io as skio

from mibitracker.request_helpers import MibiRequests

DEBUG = 0
#DEBUG = 1

#SAVE = True
SAVE = False

#UPLOAD_TO_MIBITRACKER = True
UPLOAD_TO_MIBITRACKER = False

# open mibi request
if UPLOAD_TO_MIBITRACKER:
    from dotenv import load_dotenv
    fname_login = '/path/to/MIBItracker_login.dat'
    load_dotenv(fname_login)
    mr = MibiRequests('https://backend-dot-mibitracker-internal.appspot.com',
                      email=os.getenv('MIBITRACKER_EMAIL'),
                      password=os.getenv('MIBITRACKER_PASSWORD'))

###########################################################################

def upload_channel_to_mibitracker(image, channel_label, image_id):

    print(f'Uploading channel label: {channel_label}')
    buf = io.BytesIO()
    skio.imsave(buf, image)
    buf.seek(0)
    #if UPLOAD_TO_MIBITRACKER:
    #    mr.upload_channel(image_id, buf, f'{channel_label}.png')

###########################################################################

# get image from mibitracker

run_name = '20180121_1250_1251'
point_name = 'Point2'
image_id = mr.image_id(run_name, point_name)
print(f'image ID: {image_id}')
image = mr.get_mibi_image(image_id)
print(f'channels: {image.channels}')
print(f'metadata: {image.metadata}')

# duplicate channel
image_89_dup = image[89]
#channel_mass_89_dup = 289
#channel_label_89_dup = 'dsDNA_dup_289'
channel_label_89_dup = 'dsDNA_dup'

if UPLOAD_TO_MIBITRACKER:
    print('Uploading channels to mibitracker.')
    image_id = mr.image_id(run_name, point_name)
    print(f'run: {run_name}, point: {point_name}, image ID: {image_id}')
    upload_channel_to_mibitracker(image=image_89_dup,
                                  channel_label=channel_label_89_dup,
                                  image_id=image_id)
