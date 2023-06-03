#!/usr/bin/env python

# authored by ChatGPT

import cv2
import numpy as np
import sys
import os

# Constants
THRESHOLD = 0.8  # Text change threshold (adjust as needed)

# Function to compare two images and determine if they are different
def images_are_different(img1, img2):
	difference = cv2.absdiff(img1, img2)
	gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
	_, threshold = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
	contours, _ = cv2.findContours(
		threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
	)
	return len(contours) > 0

# Function to extract the timestamp from the video frame
def extract_timestamp(video, frame_index):
	total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
	total_seconds = total_frames / video.get(cv2.CAP_PROP_FPS)
	current_seconds = frame_index / video.get(cv2.CAP_PROP_FPS)
	minutes = int(current_seconds // 60)
	seconds = int(current_seconds % 60)
	return f"{minutes:02d}:{seconds:02d}"

# Parse command line arguments
if len(sys.argv) != 10:
	print("Usage: python script.py video_path x1 y1 w1 h1 x2 y2 w2 h2")
	sys.exit(1)

video_path = sys.argv[1]
fixed_areas = [
	tuple(map(int, sys.argv[2:6])),  # First fixed area coordinates (x1, y1, w1, h1)
	tuple(map(int, sys.argv[6:])),  # Second fixed area coordinates (x2, y2, w2, h2)
]

# Open the video file
video = cv2.VideoCapture(video_path)

# Initialize variables
chapter_lists = [[] for _ in fixed_areas]
prev_frames_areas = [None] * len(fixed_areas)
frame_index = 0

# Create output directory if it doesn't exist
output_dir = "output_frames/"
os.makedirs(output_dir, exist_ok=True)

# Iterate through each frame of the video
while True:
	success, frame = video.read()
	if not success:
		break

	# Process each fixed area
	for i, fixed_area in enumerate(fixed_areas):
		# Unpack the fixed area coordinates
		x, y, w, h = fixed_area

		# Crop the frame to the fixed area
		frame_area = frame[y : y + h, x : x + w]

		# Compare the current frame area with the previous frame area
		if (
			prev_frames_areas[i] is not None
			and images_are_different(frame_area, prev_frames_areas[i])
		):
			timestamp = extract_timestamp(video, frame_index)
			chapter_lists[i].append(timestamp)

			# Save the frame
			output_path = f"{output_dir}chapter_{i+1}_{timestamp.replace(':', '_')}.jpg"
			cv2.imwrite(output_path, frame_area)

		# Update the previous frame area
		prev_frames_areas[i] = frame_area

	# Display the current frame with the fixed areas
	for fixed_area in fixed_areas:
		x, y, w, h = fixed_area
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imshow("Video", frame)
	if cv2.waitKey(1) == ord("q"):
		break

	# Increment the frame index
	frame_index += 1

# Release the video capture and close any open windows
video.release()
cv2.destroyAllWindows()

# Print the chapter lists
for i, chapter_list in enumerate(chapter_lists):
	print(f"Chapter List {i+1}:")
	for chapter in chapter_list:
		print(chapter)
	print()
