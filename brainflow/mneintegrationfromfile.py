import time

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

import mne


def main():
    BoardShim.enable_dev_board_logger()
    # use synthetic board for demo
    params = BrainFlowInputParams()
    params.file = "/home/ignacio/Downloads/3D-322(B)/Open BCI_2D/BrainFlow-RAW_2024-09-30_16-14-37_0.csv"
    #params.file_aux = "streamer_aux.csv"
    params.master_board = BoardIds.CYTON_DAISY_BOARD
    board_id = BoardIds.PLAYBACK_FILE_BOARD.value
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    time.sleep(10)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(params.master_board)
    eeg_data = data[eeg_channels, :]
    eeg_data = eeg_data / 1000000  # BrainFlow returns uV, convert to V for MNE

    # Creating MNE objects from brainflow data arrays
    ch_types = ['eeg'] * len(eeg_channels)
    ch_names = BoardShim.get_eeg_names(params.master_board)
    sfreq = BoardShim.get_sampling_rate(params.master_board)
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    raw = mne.io.RawArray(eeg_data, info)
    # its time to plot something!
    #raw.plot_psd(average=True)
    raw.compute_psd().plot(average=True)
    plt.savefig('psd.png')


if __name__ == '__main__':
    main()

