import os

import numpy as np

from mibidata import tiff
from mibidata import mibi_image as mi

#SAVE_OUTPUT = True
SAVE_OUTPUT = False

OLD_METADATA = {
    'run': '20191113_random_old_metadata', 'date': '2019-11-13T16:56:00',
    'coordinates': (12345, -67890), 'size': 500., 'slide': '857',
    'point_name': 'Random_Data', 'dwell': 4, 'scans': '0,5',
    'folder': 'Point1/RowNumber0/Depth_Profile0',
    'aperture': '300um', 'instrument': 'MIBIscope1', 'tissue': 'Random',
    'panel': '20100101_1x', 'version': None, 'mass_offset': 0.1,
    'mass_gain': 0.2, 'time_resolution': 0.5, 'miscalibrated': False,
    'check_reg': False, 'filename': '20191113_random_old_metadata'
}

# create MibiImage with random data
np.random.seed(2468)
random_channel_data = np.random.randint(0, 65535, (128, 128, 3), dtype=np.uint16)
channels = ['Channel 1', 'Channel 2', 'Channel 3']
random_mibi_image = mi.MibiImage(
    random_channel_data, channels,
    **OLD_METADATA)
# INFO: use old software if tiff should be saved with old metadata format
#       (before version '1.0')

# save a tiff
out_file_name = random_mibi_image.filename + '.tiff'
if SAVE_OUTPUT:
    print(f'Saving image to {out_file_name}')
    tiff.write(out_file_name, new_image)
