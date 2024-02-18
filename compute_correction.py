import numpy as np


def compute_correction(
    weld_start,
    weld_end,
    teo_sensing_point_1,
    real_sensing_point_1,
    teo_sensing_point_2,
    real_sensing_point_2,
):

    offset_1 = real_sensing_point_1 - teo_sensing_point_1
    offset_2 = real_sensing_point_2 - teo_sensing_point_2

    weld_start_corrected = weld_start
    weld_end_corrected = weld_end
    weld_start_corrected[0] = weld_start[0] + offset_1[0]
    weld_end_corrected[0] = weld_end[0] + offset_1[0]

    return weld_start_corrected, weld_end_corrected
