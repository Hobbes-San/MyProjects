class Config:

    #########################################################################
    # Game configuration

    # Name of the game, with version (e.g. PongDeterministic-v0)
    ATARI_GAME = 'SpaceInvaders-v0'

    # Enable to see the trained agent in action
    PLAY_MODE = False
    # Enable to train
    TRAIN_MODELS = True

    #########################################################################
    # Number of agents, predictors, trainers and other system settings
    
    # If the dynamic configuration is on, these are the initial values.
    # Number of Agents
    AGENTS = 32
    # Number of Predictors
    PREDICTORS = 2
    # Number of PG Trainers
    PG_TRAINERS = 4
    #Number of QL Trainers
    QL_TRAINERS = 1

    # Device
    DEVICE = 'gpu:0'

    #########################################################################
    # Algorithm parameters

    # Discount factor
    DISCOUNT = 1
    
    # Tmax
    TIME_MAX = 5
    
    # Reward Clipping
    REWARD_MIN = -1
    REWARD_MAX = 1

    # Parameters for the PG queue and the QL replay buffer
    MAX_BUFFER_SIZE = 4000
    MIN_BUFFER_SIZE = 3500
    MAX_QUEUE_SIZE = 100
    QL_BATCH_SIZE = 32
    
    PREDICTION_BATCH_SIZE = 128

    # Input of the DNN
    STACKED_FRAMES = 4
    IMAGE_WIDTH = 84
    IMAGE_HEIGHT = 84

    # Total number of episodes
    EPISODES = 30000

    # Entropy regualrization hyper-parameter
    BETA_START = 0.01
    BETA_END = 0.01

    # Learning rate
    LEARNING_RATE_START = 0.0003
    LEARNING_RATE_END = 0.0003

    # RMSProp parameters
    RMSPROP_DECAY = 0.99
    RMSPROP_MOMENTUM = 0.0
    RMSPROP_EPSILON = 0.1
    
    # Gradient clipping
    USE_GRAD_CLIP = True
    GRAD_CLIP_NORM = 40.0 
    # Epsilon (regularize policy lag in GA3C)
    LOG_EPSILON = 1e-6
    # Training min batch size - increasing the batch size increases the stability of the algorithm, but make learning slower
    PG_TRAINING_MIN_BATCH_SIZE = 30
    
    #########################################################################
    
    # Print stats every PRINT_STATS_FREQUENCY episodes
    PRINT_STATS_FREQUENCY = 100
    # The window to average stats
    STAT_ROLLING_MEAN_WINDOW = 1000

    # Results filename
    RESULTS_FILENAME = 'results.txt'
    # Network checkpoint name
    NETWORK_NAME = 'network'
