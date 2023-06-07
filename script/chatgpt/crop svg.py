#!/usr/bin/env python

# authored by ChatGPT

from svgpathtools import svg2paths, Path, wsvg
import argparse

def crop_svg(input_file, output_file, buffer_size):
	# Load the SVG file as a list of paths
	paths, attributes = svg2paths(input_file)

	# (not authored by ChatGPT)
	if not 'd' in attributes[-1]:
		print('removed back', paths.pop(), attributes.pop())

	# Find the bounds of all paths
	min_x, min_y, max_x, max_y = paths[0].bbox()
	for path in paths[1:]:
		x1, y1, x2, y2 = path.bbox()
		if x1 < min_x:
			min_x = x1
		if y1 < min_y:
			min_y = y1
		if x2 > max_x:
			max_x = x2
		if y2 > max_y:
			max_y = y2

	# Move the paths to the upper left corner
	for path in paths:
		path = path.translated(complex(-min_x + buffer_size, -min_y + buffer_size))

	# Write the cropped SVG file
	wsvg(paths, attributes=attributes, filename=output_file)

if __name__ == '__main__':
	# Define command line arguments
	parser = argparse.ArgumentParser(description='Crop SVG file by moving paths to upper left corner')
	parser.add_argument('input_file', help='Input SVG file')
	parser.add_argument('output_file', help='Output SVG file')
	parser.add_argument('--buffer', type=float, default=0.1, help='Buffer size in SVG units')

	# Parse arguments and call the crop function
	args = parser.parse_args()
	crop_svg(args.input_file, args.output_file, args.buffer)
