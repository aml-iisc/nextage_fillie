import numpy as np

# Sample masked RGB image (4x3)
masked_rgb_image = np.array([[100, 150, 200],
                             [50, 75, 100],
                             [25, 50, 75],
                             [150, 200, 250],
                             [100, 150, 200],
                             [50, 75, 100],
                             [25, 50, 75],
                             [150, 200, 250],
                             [100, 150, 200],
                             [50, 75, 100],
                             [25, 50, 75],
                             [150, 200, 250]])

# Calculate the average of each color channel
average_channel_values = np.mean(masked_rgb_image, axis=0)
print(masked_rgb_image.shape)
# Display the average channel values
print("Average Channel Values (R, G, B):", average_channel_values)
