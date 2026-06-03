## paths
RAW_FRAMES = "data/raw_data/raw_frames"
IDLE = "data/raw_data/idle"
BITE = "data/raw_data/bite"
SKIPPED = "data/raw_data/skipped"

DATASET_STR = "data/dataset"
FINAL_IDLE = "data/dataset/idle"
FINAL_BITE = "data/dataset/bite"

PRED_IDLE = "data/prediction/idle"
PRED_BITE = "data/prediction/bite"

# live capture screen positioning
collector_monitor = {
    "top": 490,
    "left": 330,
    "width": 300,
    "height": 300
}

# CNN model configs
MODEL_PATH = "models/bite_cnn_beta.pth"

IMAGE_SIZE = 128
class_names = ["bite", "idle"]

CAST_DELAY = 2.5     
REEL_DELAY = 2.5   
BITE_THRESHOLD = 0.90
PREDICTION_INTERVAL = 0.2 