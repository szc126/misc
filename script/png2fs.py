#!/usr/bin/env python3

# convert png to fontstruct
# paste script output into clipboard

from PIL import Image
import sys
import json
import pyperclip # instead of escaping quote characters with subprocess so hard i reach terminal velocity
import copy

image = Image.open(sys.argv[1])
pixels = image.load()

glyph_width = 8 # x
glyph_height = 16 # y

fs_glyph_template = json.loads("""
{"id":"99999999-9999-9999-9999-999999999999","type":"MultiLayerSelection","value":{"layers":{"99999":[
]},"palette":[{"cid":999,"pos":1,"order":1,"brick_id":1,"id":99999999}]}}
""")
fs_brick_template = json.loads("""
{"x":9,"y":9,"tx":0,"ty":0,"br":0,"r":0,"sx":1,"sy":1}
""")

x_position = 0
while x_position < image.size[0]:
	fs_glyph_local = copy.deepcopy(fs_glyph_template)
	for y in range(0, glyph_height):
		row = ''
		row_d = ''
		for x in range(x_position, x_position + glyph_width):
			if (
				isinstance(pixels[x, y], tuple) and pixels[x, y] < (100, 100, 100)
			) or (
				isinstance(pixels[x, y], int) and pixels[x, y] == 1
			):
				row += '鬱'
				fs_brick_local = copy.deepcopy(fs_brick_template)
				fs_brick_local['x'] = x - x_position
				fs_brick_local['y'] = glyph_height - y - 1
				fs_glyph_local['value']['layers']['99999'].append(fs_brick_local)
			else:
				row += '　'
			row_d += str(pixels[x, y])
		print(row)
		#print(row_d)
	pyperclip.copy('localStorage.setItem(\'clipboard\', JSON.stringify(' + json.dumps(fs_glyph_local) + '));')
	input('...')

	x_position += glyph_width