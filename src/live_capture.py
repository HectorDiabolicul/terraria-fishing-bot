import cv2
import numpy as np
from mss import mss
import pyautogui
import time

import torch
from PIL import Image

from src.config import collector_monitor, class_names, PREDICTION_INTERVAL, BITE_THRESHOLD, REEL_DELAY, CAST_DELAY
from src.model_loader import test_transform, model


### LIVE SCREEN -----------------------------------------------------------------------------------

sct = mss()

window_name = "Live Bobber Capture"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Move mouse to corner to stop pyautogui in emergency
pyautogui.FAILSAFE = True

state = "WAITING"
last_action_time = time.time()
last_prediction_time = 0
bite_armed = True

bite_prob = 0.0
idle_prob = 0.0
predicted_class = "waiting"
confidence = 0.0

while True:
    screenshot = sct.grab(collector_monitor)

    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    now = time.time()
    prediction_updated = False

    if now - last_prediction_time >= PREDICTION_INTERVAL:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)

        image_tensor = test_transform(pil_image)
        image_tensor = image_tensor.unsqueeze(0)

        with torch.no_grad():
            output = model(image_tensor)
            probabilities = torch.softmax(output, dim=1)

            bite_prob = probabilities[0][0].item()
            idle_prob = probabilities[0][1].item()

            prediction = output.argmax(dim=1).item()
            predicted_class = class_names[prediction]
            confidence = probabilities[0][prediction].item()

        last_prediction_time = now  
        prediction_updated = True

    match state: 
        case "WAITING":
            if prediction_updated and bite_prob < BITE_THRESHOLD:
                bite_armed = True

            if prediction_updated and bite_armed and bite_prob >= BITE_THRESHOLD:
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()

                bite_armed = False
                state = "REELING"
                last_action_time = now
        case "REELING":
            if now - last_action_time >= REEL_DELAY:
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()

                bite_prob = 0.0
                idle_prob = 0.0
                bite_armed = False
                state = "CASTING"
                last_action_time = now
        case "CASTING":
            if now - last_action_time >= CAST_DELAY:
                state = "WAITING"
    
    text1 = f"state: {state}"
    text2 = f"pred: {predicted_class} {confidence:.2%}"
    cv2.putText(frame, text1, (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2)
    cv2.putText(frame, text2, (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2)

    cv2.imshow(window_name, frame)

    if cv2.waitKey(16) & 0xFF == ord("q"):
        break
    

cv2.destroyAllWindows()
