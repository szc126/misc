#!/usr/bin/env python3

# extract files from a har archive
# exported from the firefox network tab

import sys
import json
import base64
from haralyzer import HarParser, HarPage

with open(sys.argv[1], 'r') as file:
	har_parser = HarParser(json.loads(file.read()))
	for har_page in har_parser.pages:
		for i, har_entry in enumerate(har_page.entries):
			print(har_entry.url)
			print('\t' + har_entry.url.split('?')[0].split('/')[-1])
			try:
				with open(sys.argv[1].removesuffix('.har').split('/')[-1] + '.' + har_entry.url.split('?')[0].split('/')[-1], 'wb') as file_out:
					file_out.write(base64.b64decode(har_entry.response.text))
			except ValueError:
				with open(sys.argv[1].removesuffix('.har').split('/')[-1] + '.' + har_entry.url.split('?')[0].split('/')[-1], 'w') as file_out:
					file_out.write(har_entry.response.text)