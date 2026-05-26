from pathlib import Path
import cv2
import shutil

from src.config import RAW_FRAMES, IDLE, BITE, SKIPPED
Path(RAW_FRAMES).mkdir(parents=True,exist_ok=True)
Path(IDLE).mkdir(parents=True,exist_ok=True)
Path(BITE).mkdir(parents=True,exist_ok=True)
Path(SKIPPED).mkdir(parents=True,exist_ok=True)

images = sorted(Path(RAW_FRAMES).glob("*.png"))

for image_path in images:
    frame = cv2.imread(str(image_path))

    cv2.putText(frame, "I=idle | B=bite | S=skip | Q=quit", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Sort images", frame)

    key = cv2.waitKey(0) & 0xFF
    match chr(key):
        case "i":
            target = IDLE
        case "b":
            target = BITE
        case "s":
            target = SKIPPED
        case "q":
            break
        case _:
            continue

    new_id = len(list(Path(target).glob("*.png")))
    new_filename = f"frame_{new_id:04d}.png"        ## i use 0001, 0002 ... to not conflict with current frames

    shutil.move(str(image_path),str(f"{target}/{new_filename}"))
    print(f"Moved: {image_path.name} -> {target}")

cv2.destroyAllWindows()
    
