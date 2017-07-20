import sys
import warnings
if sys.version_info < (3,0):
    warnings.warn("Optimized for Python3. Performance may suffer under Python2.", Warning)

import gym

from Config import Config
from Server import Server

# Parse arguments
for i in range(1, len(sys.argv)):
    # Config arguments should be in format of Config=Value
    # For setting booleans to False use Config=
    x, y = sys.argv[i].split('=')
    setattr(Config, x, type(getattr(Config, x))(y))

# Adjust configs for Play mode
if Config.PLAY_MODE:
    Config.AGENTS = 1
    Config.PREDICTORS = 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    Config.PG_TRAINERS = 1
    Config.DQ_TRAINERS = 1
    Config.DYNAMIC_SETTINGS = False

    Config.LOAD_CHECKPOINT = True
    Config.TRAIN_MODELS = False
    Config.SAVE_MODELS = False

gym.undo_logger_setup()

# Start main program
Server().main()
