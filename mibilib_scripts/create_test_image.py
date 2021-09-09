import os

import numpy as np

from mibidata import tiff
from mibidata import mibi_image as mi

#SAVE_OUTPUT = True
SAVE_OUTPUT = False

DATA = np.arange(500).reshape(10, 10, 5).astype(np.uint16)
CHANNELS = ((1, 'Target1'), (2, 'Target2'), (3, 'Target3'),
            (4, 'Target4'), (5, 'Target5'))
OLD_METADATA = {
    'run': '20180703_1234_test', 'date': '2017-09-16T15:26:00',
    'coordinates': (12345, -67890), 'size': 500., 'slide': '857',
    'point_name': 'R1C3_Tonsil', 'dwell': 4, 'scans': '0,5',
    'folder': 'Point1/RowNumber0/Depth_Profile0',
    'aperture': '300um', 'instrument': 'MIBIscope1', 'tissue': 'Tonsil',
    'panel': '20170916_1x', 'version': None, 'mass_offset': 0.1,
    'mass_gain': 0.2, 'time_resolution': 0.5, 'miscalibrated': False,
    'check_reg': False, 'filename': '20180703_1234_test'
}

image = mi.MibiImage(DATA, CHANNELS, **OLD_METADATA)
# INFO: use old software if tiff should be saved with old metadata format
#       (before MIBItiff version '1.0'), so mibitracker-client of late
#       October 2019 should be fine.

# save a tiff
out_filename = image.filename + '_old_metadata.tiff'
if SAVE_OUTPUT:
    print(f'Saving image to {out_filename}')
    tiff.write(out_filename, image)
