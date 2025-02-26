import cv2
import numpy as np

# Load the image
image_path = "14.jpg"  # Change if needed
image = cv2.imread(image_path)

# Convert to Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur (reduces noise)
blurred = cv2.GaussianBlur(gray, (5,5), 0)

# Apply Adaptive Thresholding
threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Perform Dilation and Erosion (removes small noise)
kernel = np.ones((2,2), np.uint8)
processed_image = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

# Save the processed image for OCR
processed_image_path = "processed.jpg"
cv2.imwrite(processed_image_path, processed_image)

print(f"✅ Preprocessing complete! Saved as {processed_image_path}")
