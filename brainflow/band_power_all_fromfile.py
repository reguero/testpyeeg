import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter


def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value
    params.file = "/home/ignacio/Downloads/3D-322(B)/Open BCI_2D/BrainFlow-RAW_2024-09-30_16-14-37_0.csv"
    params.master_board = BoardIds.CYTON_DAISY_BOARD
    board_id = BoardIds.PLAYBACK_FILE_BOARD.value
    sampling_rate = BoardShim.get_sampling_rate(params.master_board)
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(params.master_board)
    bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)
    print("avg band powers : %s" % str(bands[0]))
    print("stddev band powers : %s" % str(bands[1]))


if __name__ == "__main__":
    main()
