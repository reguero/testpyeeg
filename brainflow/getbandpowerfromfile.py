import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, WindowOperations, DetrendOperations


def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    params.file = "/home/ignacio/Downloads/3D-322(B)/Open BCI_2D/BrainFlow-RAW_2024-09-30_16-14-37_0.csv"
    #params.file_aux = "streamer_aux.csv"
    params.master_board = BoardIds.CYTON_DAISY_BOARD
    board_id = BoardIds.PLAYBACK_FILE_BOARD.value
    board_descr = BoardShim.get_board_descr(params.master_board)
    sampling_rate = int(board_descr['sampling_rate'])
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    eeg_channels = board_descr['eeg_channels']
    # second eeg channel of synthetic board is a sine wave at 10Hz, should see huge alpha
    eeg_channel = eeg_channels[1]
    # optional detrend
    DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
    psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                   WindowOperations.BLACKMAN_HARRIS.value)

    band_power_alpha = DataFilter.get_band_power(psd, 7.0, 13.0)
    band_power_beta = DataFilter.get_band_power(psd, 14.0, 30.0)
    print("alpha/beta:", band_power_alpha / band_power_beta)


if __name__ == "__main__":
    main()
