from pathlib import Path
import cv2
import shutil

from src.config import IDLE, SKIPPED, FINAL_IDLE, PRED_IDLE
Path(FINAL_IDLE).mkdir(parents=True,exist_ok=True)
Path(PRED_IDLE).mkdir(parents=True,exist_ok=True)
Path(SKIPPED).mkdir(parents=True,exist_ok=True)

images = sorted(Path(IDLE).glob("*.png"))

for image_path in images:
    frame = cv2.imread(str(image_path))

    cv2.putText(frame, "I=idle | S=skip | P=pred | Q=quit", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Sort images", frame)

    key = cv2.waitKey(0) & 0xFF
    match chr(key):
        case "i":
            target = FINAL_IDLE
        case "s":
            target = SKIPPED
        case "p":
            target = PRED_IDLE
        case "q":
            break
        case _:
            continue

    new_id = len(list(Path(target).glob("*.png")))
    new_filename = f"idle_{new_id:05d}.png"        

    shutil.move(str(image_path),str(f"{target}/{new_filename}"))
    print(f"Moved: {image_path.name} -> {target}")

cv2.destroyAllWindows()
    
