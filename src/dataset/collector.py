import cv2
import numpy as np
from mss import mss
from pathlib import Path
import time

from src.config import RAW_FRAMES, collector_monitor

sct = mss()

Path(RAW_FRAMES).mkdir(exist_ok=True, parents=True) ## create dir if not exists
frame_id = len(list(Path(RAW_FRAMES).glob("*.png")))    ## for naming frames (ex: frame_1, frame_2...) without losing track when restarting

window_name = "Terraria Capture"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

last_saved = time.time()
save_interval = 0.2     ## 5 frames/sec

while True:
    screenshot = sct.grab(collector_monitor)

    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    now = time.time()
    if now - last_saved >= save_interval:
        filename = f"{RAW_FRAMES}/frame_{frame_id:05d}.png"     ## 00001, 00002
        cv2.imwrite(filename, frame)

        print(f"Saved: frame_{frame_id}")
        last_saved = now
        frame_id += 1

    cv2.imshow(window_name, frame)

    if cv2.waitKey(16) & 0xFF == ord("q"):      ## press 'q' to quit
        break

cv2.destroyAllWindows()