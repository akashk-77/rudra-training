import cv2
import numpy as np

# Load the coin image
image = cv2.imread('image.jpg')

if image is None:
    print("Error: Could not load image. Make sure 'image.jpeg' exists.")
    exit()

# 1. Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. Apply Median Blur to smooth inner coin engravings without blurring edges
blurred = cv2.medianBlur(gray, 7)

# 3. Apply Hough Circle Transform with fixed parameters tailored for this coin grid
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.2,          # Accumulator resolution ratio
    minDist=50,      # Minimum distance between detected coin centers (prevents overlapping circles)
    param1=50,       # Upper Canny edge detector threshold
    param2=35,       # Accumulator threshold (higher value prevents inner engravings from triggering false circles)
    minRadius=28,    # Minimum expected coin radius in pixels
    maxRadius=55     # Maximum expected coin radius in pixels
)

# 4. Draw detected circles
if circles is not None:
    # Round coordinates to integers
    circles = np.uint16(np.around(circles))
    
    print(f"--- Detected {len(circles[0])} Coins ---")
    
    for i, (x, y, r) in enumerate(circles[0, :], start=1):
        print(f"Coin #{i} -> Center: ({x}, {y}), Radius: {r}")
        
        # Draw green outer circle outline
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)
        
        # Draw red center point
        cv2.circle(image, (x, y), 2, (0, 0, 255), 3)

    print(f"\nTotal Coins Found: {len(circles[0])}")
else:
    print("No circles detected with current parameters.")

# Display the result
cv2.imshow("Hough Circles Coin Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
