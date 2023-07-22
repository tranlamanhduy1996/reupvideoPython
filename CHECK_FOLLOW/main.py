import os

from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import VideoClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx import resize

# Load the two video files
# Path to the folder containing the videos
# folder_path = "G:\\My Drive\\VIDEO_CHUA_EDIT"
folder_path = "C:\\Users\\ADMIN\\Desktop\\Video\\VideoBeforeEdit"
video_goc = VideoFileClip("C:\\Users\\ADMIN\\Desktop\\Video\\video_goc.mp4")
video_goc_dai = VideoFileClip("C:\\Users\\ADMIN\\Desktop\\Video\\video_goc_dai.mp4")

# Get a list of files in the folder
file_list = os.listdir(folder_path)

# Sort the files to ensure sequential processing
file_list.sort()

count = 1
for file_name in file_list:

    # Create the full path to the video file
    file_path = os.path.join(folder_path, file_name)

    # Load the video file as a clip
    video = VideoFileClip(file_path)

    # Caculate diff between 2 video
    duration_diff = video_goc.duration - video.duration

    if(duration_diff > 0):

        split_clip = video_goc.subclip(0, video.duration + 1)
    else:
        split_clip = video_goc_dai.subclip(0, video.duration + 1)

    desired_height = split_clip.h // 1.2

    # Resize the first video to match the dimensions of the second video
    video1_resized = video.resize(height=desired_height)

    x_position = (video_goc.w - video1_resized.w) // 2
    y_position = (video_goc.h - video1_resized.h) // 2

    # Set the start time of video 1 to 1 second
    video1_resized = video1_resized.set_start(1)

    # Overlay video 1 onto video 2
    if(video1_resized.w > split_clip.w):
        new_width = 1080
        resized_clip = resize.resize(video1_resized, width=new_width)
        clip2 = resized_clip.crossfadein(1.0)
        video_combined = CompositeVideoClip([split_clip, clip2.set_position((0, y_position))])
    else:
        new_width = 1080
        resized_clip = resize.resize(video1_resized, width=new_width)
        # Define the dimensions of the square crop.
        crop_width = 1080
        crop_height = 1080

        # Get the center of the resized_clip.
        center_x = resized_clip.w / 2
        center_y = resized_clip.h / 2

        # Calculate the coordinates for the top-left corner of the crop rectangle.
        x1 = center_x - crop_width / 2
        y1 = center_y - crop_height / 2

        # Calculate the coordinates for the bottom-right corner of the crop rectangle.
        x2 = center_x + crop_width / 2
        y2 = center_y + crop_height / 2
        cropped_clip = resized_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        clip2 = cropped_clip.crossfadein(1.0)
        video_combined = CompositeVideoClip([split_clip, clip2.set_position((0, y_position))])

    name_video = "C:\\Users\\ADMIN\\Desktop\\Video\\VideoAfterEdit\\video.mp4"
    # Save the resulting video
    video_combined.write_videofile(name_video, codec="libx264")

    count += 1


