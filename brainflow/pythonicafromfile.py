import time
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
from brainflow.data_filter import DataFilter


def main():
    board_id = BoardIds.SYNTHETIC_BOARD
    params = BrainFlowInputParams()
    params.file = "/home/ignacio/Downloads/3D-322(B)/Open BCI_2D/BrainFlow-RAW_2024-09-30_16-14-37_0.csv"
    #params.file_aux = "streamer_aux.csv"
    params.master_board = BoardIds.CYTON_DAISY_BOARD
    board_id = BoardIds.PLAYBACK_FILE_BOARD.value

    eeg_channels = BoardShim.get_eeg_channels(params.master_board)

    #params = BrainFlowInputParams()
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    time.sleep(10)
    data = board.get_board_data(500)
    board.stop_stream()
    board.release_session()

    channel_to_use = eeg_channels[4]
    data = data[channel_to_use, :]
    # provide 5 chunks of data for components selection
    data = data.reshape(5, 100)
    data = np.ascontiguousarray(data)
    w, k, a, s = DataFilter.perform_ica(data, 2)
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(s[0, :])
    axs[0].set_title('Unmixed signal 1')
    axs[1].plot(s[1, :])
    axs[1].set_title('Unmixed signal 2')
    plt.savefig('unmixed_signal.png')


if __name__ == "__main__":
    main()
