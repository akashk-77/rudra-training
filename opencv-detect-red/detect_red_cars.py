import cv2
import numpy as np

# Load the image (using image.jpeg)
image = cv2.imread('1.jpg')

if image is None:
    print("Error: Could not load image. Make sure 'image.jpeg' exists in this directory.")
    exit()

# Convert BGR image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Red hue spans across the boundary of the HSV spectrum (0-10 and 170-180)
lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])

# Combine red color ranges
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)

# Clean up noise with morphological operations
kernel = np.ones((5, 5), np.uint8)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_DILATE, kernel)

# Find contours for red objects
contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small noise like tail lights by setting a minimum area threshold
min_area = 1000  
found_cars = 0

print("--- Detected Red Vehicles ---")
for contour in contours:
    if cv2.contourArea(contour) > min_area:
        found_cars += 1
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate bounding box points
        x1, y1 = x, y
        x2, y2 = x + w, y + h
        
        print(f"Red Car #{found_cars}: Top-Left: ({x1}, {y1}), Bottom-Right: ({x2}, {y2}), Width: {w}, Height: {h}")
        
        # Draw red box (BGR format: Blue=0, Green=0, Red=255)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

if found_cars == 0:
    print("No red cars detected based on current thresholds.")

# Display final result
cv2.imshow("Red Car Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
