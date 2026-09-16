import cv2
import numpy as np

# Load image
image = cv2.imread('coins.jpeg')

if image is None:
    print("Error: Could not load image.")
    exit()

# Step 1: Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Apply Gaussian Blur to reduce noise (critical for Hough Circles)
gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Step 3: Apply Hough Circle Transform
# cv2.HOUGH_GRADIENT is the standard detection method
circles = cv2.HoughCircles(
    gray_blurred, 
    cv2.HOUGH_GRADIENT, 
    dp=1.2,             # Inverse ratio of accumulator resolution
    minDist=30,         # Minimum distance between detected centers
    param1=50,          # Upper threshold for internal Canny edge detector
    param2=30,          # Accumulator threshold for circle centers (lower = more false circles)
    minRadius=10,       # Minimum circle radius in pixels
    maxRadius=100       # Maximum circle radius in pixels
)

# Step 4: Draw circles and extract coordinates
if circles is not None:
    # Round coordinates to integers
    circles = np.uint16(np.around(circles))
    
    print(f"--- Detected {len(circles[0])} Circle(s) ---")
    
    for i, (x, y, r) in enumerate(circles[0, :], start=1):
        print(f"Circle #{i} -> Center: ({x}, {y}), Radius: {r}")
        
        # Draw outer circle (Green outline, BGR: 0, 255, 0)
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)
        
        # Draw center point (Red dot, BGR: 0, 0, 255)
        cv2.circle(image, (x, y), 2, (0, 0, 255), 3)

    cv2.imshow('Detected Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No circles detected.")
