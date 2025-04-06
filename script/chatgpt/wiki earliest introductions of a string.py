#!/usr/bin/env python

# authored by ChatGPT

import mwxml
from datetime import datetime

def find_earliest_occurrences(dump_path, search_string, limit=20):
	occurrences = []

	dump = mwxml.Dump.from_file(open(dump_path, 'rb'))
	for page in dump:
		for revision in page:
			if revision.text and search_string.lower() in revision.text.lower():
				revision_timestamp = revision.timestamp
				occurrences.append((revision_timestamp, revision))

	# Sort occurrences by timestamp
	occurrences.sort(key=lambda x: x[0])

	# Print the first 'limit' occurrences
	for timestamp, revision in occurrences[:limit]:
		print(f"Occurrence of '{search_string}' found in page '{revision.page.title}' at revision ID {revision.id}, timestamp: {revision.timestamp}")

	if not occurrences:
		print(f"'{search_string}' not found in the dump.")

# Replace 'your-dump-file.xml' with the path to your MediaWiki dump file
# Replace 'your-search-string' with the string you want to find
dump_path = 'your-dump-file.xml'
search_string = 'your-search-string'

find_earliest_occurrences(dump_path, search_string)
