#!/usr/bin/env python3

# extract files from a har archive
# exported from the firefox network tab

import sys
import json
import base64
import os
from haralyzer import HarParser, HarPage

with open(sys.argv[1], 'r') as file:
	har_parser = HarParser(json.loads(file.read()))
	for har_page in har_parser.pages:
		for i, har_entry in enumerate(har_page.entries):
			print(har_entry.url)

			har_basename = sys.argv[1].removesuffix('.har').split('/')[-1]
			url_basename = har_entry.url.split('?')[0].split('/')[-1]
			filename = har_basename + '.' + url_basename

			if os.path.exists(filename):
				filename += '.' + str(i)

			print(filename)

			try:
				with open(filename, 'wb') as file_out:
					file_out.write(base64.b64decode(har_entry.response.text))
			except ValueError:
				with open(filename, 'w') as file_out:
					file_out.write(har_entry.response.text)