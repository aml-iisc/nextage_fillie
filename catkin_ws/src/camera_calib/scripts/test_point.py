import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Example 3D point cloud data (replace this with your actual data)
num_points = 1000
xyz_data = np.random.rand(num_points, 3)  # XYZ coordinates
rgb_data = np.random.randint(0, 255, size=(num_points, 3))  # RGB color values

# Plot the 3D point cloud with RGB colors
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot each point with its corresponding RGB color
ax.scatter(xyz_data[:, 0], xyz_data[:, 1], xyz_data[:, 2], c=rgb_data/255, marker='o', alpha=0.6)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Point Cloud with RGB Colors')

plt.show()