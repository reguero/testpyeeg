import time

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, \
    WaveletExtensionTypes, ThresholdTypes, WaveletDenoisingTypes


def main():
    BoardShim.enable_dev_board_logger()

    # use playback board for demo
    params = BrainFlowInputParams()
    params.file = "/home/ignacio/Downloads/3D-322(B)/Open BCI_2D/BrainFlow-RAW_2024-09-30_16-14-37_0.csv"
    #params.file_aux = "streamer_aux.csv"
    params.master_board = BoardIds.CYTON_DAISY_BOARD
    board_id = BoardIds.PLAYBACK_FILE_BOARD.value
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    data = board.get_current_board_data(500)
    board.stop_stream()
    board.release_session()

    # demo how to convert it to pandas DF and plot data
    eeg_channels = BoardShim.get_eeg_channels(params.master_board)
    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels].plot(subplots=True)
    plt.savefig('before_processing.png')

    # demo for denoising, apply different methods to different channels for demo
    for count, channel in enumerate(eeg_channels):
        # first of all you can try simple moving median or moving average with different window size
        if count == 0:
            DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEAN.value)
        elif count == 1:
            DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEDIAN.value)
        # if methods above dont work for your signal you can try wavelet based denoising
        # feel free to try different parameters
        else:
            DataFilter.perform_wavelet_denoising(data[channel], WaveletTypes.BIOR3_9, 3,
                                                 WaveletDenoisingTypes.SURESHRINK, ThresholdTypes.HARD,
                                                 WaveletExtensionTypes.SYMMETRIC, NoiseEstimationLevelTypes.FIRST_LEVEL)

    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels].plot(subplots=True)
    plt.savefig('after_processing.png')


if __name__ == "__main__":
    main()
