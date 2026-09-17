import cv2
import numpy as np

# Load image
image = cv2.imread('image.jpeg')

if image is None:
    print("Error: Could not load image.")
    exit()

# Step 1: Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Binary Thresholding (Invert so black circles become white shapes)
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Step 3: Find external contours of all shapes
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Step 4: Define minimum area threshold to isolate only the big circles
# Adjust this value higher/lower depending on how big a circle needs to be
min_circle_area = 2500  

count = 0
print("--- Large Circles Detected ---")

for contour in contours:
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    
    # Calculate circularity: 4 * pi * area / (perimeter^2)
    # A perfect circle equals 1.0
    circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
    
    # Filter for large size AND true circular shapes
    if area > min_circle_area and circularity > 0.7:
        count += 1
        
        # Get exact minimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        
        # Get bounding box coordinates for object detection output
        bx, by, bw, bh = cv2.boundingRect(contour)
        
        print(f"Big Circle #{count} -> Center: {center}, Radius: {radius}, Bounding Box: [X1:{bx}, Y1:{by}, X2:{bx+bw}, Y2:{by+bh}]")
        
        # Draw red bounding circle outline
        cv2.circle(image, center, radius, (0, 0, 255), 3)
        
        # Draw center red dot
        cv2.circle(image, center, 4, (0, 0, 255), -1)

print(f"\nTotal Big Circles Found: {count}")

# Save and display output
cv2.imwrite('big_circles_detected.jpg', image)
cv2.imshow("Detected Big Circles", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
