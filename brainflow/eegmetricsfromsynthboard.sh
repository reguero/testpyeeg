#!/bin/bash -x

# 2 is CYTON_DAISY_BOARD boardId
# -3 is PLAYBACK_FILE_BOARD boardId
# -1 is SYNTHETIC_BOARD boardId
#/usr/bin/python getdatafromboarexample.py --board-id -3 --file '/home/ignacio/Downloads/3D-322(B)/Open BCI_2D/BrainFlow-RAW_2024-09-30_16-14-37_0.csv' --master-board 2
/usr/bin/python eegmetricsexample.py --board-id -1

