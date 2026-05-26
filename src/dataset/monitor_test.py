import cv2
import numpy as np
from mss import mss
from pathlib import Path
import time
from src.config import collector_monitor

sct = mss()

window_name = "Terraria Capture Test"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while True:
    screenshot = sct.grab(collector_monitor)

    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    cv2.imshow(window_name, frame)

    if cv2.waitKey(16) & 0xFF == ord("q"):      ## press 'q' to quit
        break

cv2.destroyAllWindows()