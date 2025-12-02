import cv2
from ultralytics import YOLO

model = YOLO('model2.pt')

results = model('105.jpeg')
img = results[0].plot()

window_name = "Detections"
new_width = 1024
new_height = 1800

# 1. Create a named window with the WINDOW_NORMAL flag
# This flag allows the window to be resized programmatically or manually
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# 2. Resize the window to the desired dimensions (width, height)
cv2.resizeWindow(window_name, new_width, new_height)

# 3. Display the image in the window
cv2.imshow(window_name, img)
# cv2.imshow("Detections", img)
cv2.waitKey(0)
cv2.destroyAllWindows()