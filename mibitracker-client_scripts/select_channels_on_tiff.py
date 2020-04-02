import os

from mibidata import mibi_image as mi, tiff

#SAVE = True
SAVE = False

input_file_name = 'Point1_RowNumber0_Depth_Profile0.tiff'

selected_channels = [89, 113, 115, 146, 148, 149, 159, 176, 181, 197]

print(f'Reading {input_file_name}')
image = tiff.read(input_file_name)
print(f' image metadata {image.metadata()}')
print(f' image channels {image.channels}')

print(f'Selecting channels {selected_channels}')
image_selected_channels = image.slice_image(selected_channels)
print(f' selected channels image metadata {image_selected_channels.metadata()}')
print(f' selected channels image channels {image_selected_channels.channels}')

input_file_name_parts = os.path.splitext(input_file_name)
output_file_name = (input_file_name_parts[0] + '_selection' +
                    input_file_name_parts[1])

if SAVE:
    print(f'Writing {output_file_name}')
    tiff.write(output_file_name, image_selected_channels)
