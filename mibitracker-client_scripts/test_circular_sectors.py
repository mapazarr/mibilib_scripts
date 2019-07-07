import numpy as np
from numpy.testing import assert_array_equal

from mibidata import mibi_image as mi, segmentation

def test_circular_sectors():
    """Test circular sectors method in segmentation.
    """

    # create data for image 2 channels
    channels = ['ch0', 'ch1']
    data = np.stack((
        # channel 0
        np.arange(36, dtype='float').reshape(6, 6),
        # this is the matrix:
        #np.array([[ 0,  1,  2,  3,  4,  5],
        #          [ 6,  7,  8,  9, 10, 11],
        #          [12, 13, 14, 15, 16, 17],
        #          [18, 19, 20, 21, 22, 23],
        #          [24, 25, 26, 27, 28, 29],
        #          [30, 31, 32, 33, 34, 35]], dtype='float')
        # channel 1
        np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 2]], dtype='float'),
        ), axis=2)
    # assume labels are for cell ID 1, such as with label image:
    # np.array([
    #     [1, 1, 1, 1, 1, 0],
    #     [1, 1, 1, 1, 1, 0],
    #     [1, 1, 1, 1, 1, 0],
    #     [1, 1, 1, 1, 1, 0],
    #     [1, 1, 1, 1, 1, 0],
    #     [0, 0, 0, 0, 0, 0]
    # ])
    # indices of the pixels of the cell
    x = np.arange(5)
    y = x
    x_inds, y_inds = np.meshgrid(x, y, indexing='ij')
    inds = (y_inds.flatten(), x_inds.flatten())
    # sum within sectors and calculate geometric mean for each channel
    secs = []
    #for idx, val in enumerate(channels):
    for i in range(len(channels)):
        sec1 = data[2][2][i] + data[2][3][i] + data[2][4][i] + data[3][4][i]
        sec2 = data[3][3][i] + data[4][3][i] + data[4][4][i]
        sec3 = data[3][2][i] + data[4][2][i] + data[4][1][i]
        sec4 = data[3][1][i] + data[4][0][i] + data[3][0][i]
        sec5 = data[2][1][i] + data[2][0][i] + data[1][0][i]
        sec6 = data[1][1][i] + data[0][0][i] + data[0][1][i]
        sec7 = data[1][2][i] + data[0][2][i] + data[0][3][i]
        sec8 = data[1][3][i] + data[0][4][i] + data[1][4][i]
        secs_geom_mean = np.power(sec1 * sec2 * sec3 * sec4 * \
                            sec5 * sec6 * sec7 * sec8, 1/8)
        secs.append(secs_geom_mean)
    expected = np.array(secs)

    # test the function
    image = mi.MibiImage(data, channels)
    circ_secs = segmentation._circular_sectors_mean(inds,
                                                    image,
                                                    num_sectors=8)
    assert_array_equal(circ_secs, expected)

    ## test that all pixels in the cell are used
    #vals = image.data[inds]
    #import IPython; IPython.embed()
    #assert_array_equal(vals.sum(axis=0), secs.sum(axis=1))
    #assert_array_equal(vals.sum(axis=0), circ_secs.sum(axis=1))
    #assert_array_equal(vals.sum(axis=0), expected.sum(axis=1))
    #print('sum of vals: {}'.format(vals.sum(axis=0)))
    #print('sum of secs: {}'.format(secs.sum(axis=1)))

    ## compare to quadrants method
    #circ_secs_4 = segmentation._circular_sectors_mean(inds,
    #                                                  image,
    #                                                  num_sectors=4)
    #quads = segmentation._quadrant_mean(inds,
    #                                    mi.MibiImage(data, channels))
    #assert_array_equal(circ_secs_4, quads)

    # TODO: assert in secs and quads methods that nothing is left behind!!!
    # these should be equal!!!
    #    print('sum of vals: {}'.format(vals.sum(axis=0)))
    #    print('sum of secs: {}'.format(secs.sum(axis=1)))
    # same for quads!!!
    # TODO: create my own repo before committing these changes?!!!

def test_circular_sectors_small_cell():
    """Test small cell with empty sectors.
    """

    # create data for image 2 channels
    channels = ['ch0', 'ch1']
    data = np.stack((
        # channel 0
        np.arange(16, dtype='float').reshape(4, 4),
        # this is the matrix:
        #np.array([[ 0,  1,  2,  3],
        #          [ 4,  5,  6,  7],
        #          [ 8,  9, 10, 11],
        #          [12, 13, 14, 15]], dtype='float')
        # channel 1
        np.array([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]], dtype='float'),
        ), axis=2)
    # assume labels are for cell ID 1, such as with label image:
    # np.array([
    #     [0, 1, 1, 0],
    #     [0, 1, 1, 0],
    #     [0, 0, 0, 0],
    #     [0, 0, 0, 0]])
    # indices of the pixels of the cell
    inds = ((0, 0, 1, 1), (1, 2, 1, 2))
    # sum within sectors and calculate geometric mean for each channel
    secs = []
    for i in range(len(channels)):
        sec1 = 1 # empty sector
        sec2 = data[1][2][i]
        sec3 = 1 # empty sector
        sec4 = data[1][1][i]
        sec5 = 1 # empty sector
        sec6 = data[0][1][i]
        sec7 = 1 # empty sector
        sec8 = data[0][2][i]
        secs_geom_mean = np.power(sec1 * sec2 * sec3 * sec4 * \
                            sec5 * sec6 * sec7 * sec8, 1/8)
        secs.append(secs_geom_mean)
    expected = np.array(secs)

    # test the function
    image = mi.MibiImage(data, channels)
    circ_secs = segmentation._circular_sectors_mean(inds,
                                                    image,
                                                    num_sectors=8)
    assert_array_equal(circ_secs, expected)


if __name__ == '__main__':

    # call tests
    test_circular_sectors()
    test_circular_sectors_small_cell()

    #import IPython; IPython.embed()
