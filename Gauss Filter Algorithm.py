#-*- coding: utf-8 -*-
# Created on Tue Sep 8 20:04:33 2023
# @author: Luis Fernando Monjaraz Briseno

import cv2 as cv
import numpy as np
import os

# Configuration parameters
image_path = 'MH_YianGaruga.jpg'
kernel_size = 5  # Size of the Gaussian kernel (must be odd)
sigma = 1.0      # Sigma (standard deviation)

# Verify file exists
if not os.path.exists(image_path):
    print(f'Error: Image file "{image_path}" not found')
    exit()

# Load image in grayscale
image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

if image is None:
    print(f'Error: Failed to load image "{image_path}"')
    exit()

# Generate Gaussian Kernel
def generate_gaussian_kernel(size, sigma):
    """
    Generate a Gaussian kernel for image blurring.
    
    Parameters:
    - size: Kernel size (should be odd)
    - sigma: Standard deviation
    
    Returns:
    - Normalized Gaussian kernel
    """
    kernel = np.zeros((size, size), dtype='float32')
    center = (size - 1) / 2.0
    
    for x in range(size):
        for y in range(size):
            # Gaussian formula: G(x,y) = (1/(2πσ²)) * e^(-((x-x₀)² + (y-y₀)²)/(2σ²))
            diff_x = x - center
            diff_y = y - center
            exponent = -(diff_x**2 + diff_y**2) / (2 * sigma**2)
            kernel[x, y] = (1 / (2 * np.pi * sigma**2)) * np.exp(exponent)
    
    # Normalize the kernel so all values sum to 1
    kernel = kernel / np.sum(kernel)
    
    return kernel

# Generate the Gaussian kernel
gaussian_kernel = generate_gaussian_kernel(kernel_size, sigma)

# Get image dimensions
height, width = image.shape
blurred_image = np.zeros((height, width), dtype='float32')

# Apply manual convolution
print('Applying Gaussian filter...')
for i in range(height - kernel_size + 1):
    for j in range(width - kernel_size + 1):
        # Extract region of interest
        region = image[i:i + kernel_size, j:j + kernel_size].astype('float32')
        
        # Perform convolution (element-wise multiplication and sum)
        convolution_result = np.sum(region * gaussian_kernel)
        
        # Store result at the center position
        blurred_image[i + kernel_size // 2, j + kernel_size // 2] = convolution_result

# Convert back to uint8
blurred_image = np.clip(blurred_image, 0, 255).astype('uint8')

# Display results
cv.imshow('Original Image', image)
cv.imshow('Gaussian Blurred Image', blurred_image)
print('Press any key to close windows...')
cv.waitKey(0)
cv.destroyAllWindows()