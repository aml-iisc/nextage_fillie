from moviepy.editor import ImageSequenceClip

# Specify the directory containing your images
image_folder = 'images/stereoLeft/'
# Create a list of image file paths
image_files = [f'{image_folder}imageL{i}.png' for i in range(42, 150)]  # Adjust range as needed

# Create a video clip from the image sequence
clip = ImageSequenceClip(image_files, fps=20)  # Adjust fps as needed

# Write the video file
clip.write_videofile('output_video.mp4', codec='libx264')
