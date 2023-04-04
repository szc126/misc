#!/usr/bin/env python

# modified from code authored by ChatGPT

#import os
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from mutagen.id3 import ID3, TIT2, TPE1, TALB
from io import BytesIO

class MyRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		# Parse the query string
		try:
			query = urlparse(self.path).query
			params = parse_qs(query)
			url = params['url'][0]
			title = params['title'][0]
			artist = params['artist'][0]
			album = params['album'][0]
		except (KeyError, ValueError) as e:
			self.send_error(400, 'Invalid query string: ' + str(e))
			return

		# Download the MP3 file from the URL
		response = requests.get(url, stream=True)

		# Send the headers
		self.send_response(200)
		self.send_header('Content-type', 'audio/mpeg')
		self.end_headers()

		for chunk in response.iter_content(chunk_size=1024):
			if chunk:
				# Check if the chunk contains an ID3 tag
				if b'ID3' in chunk:
					# Modify the metadata of the chunk
					chunk = BytesIO(chunk)
					chunk_id3 = ID3(chunk)
					chunk_id3.add(TIT2(encoding=3, text=title))
					chunk_id3.add(TPE1(encoding=3, text=artist))
					chunk_id3.add(TALB(encoding=3, text=album))
					chunk_id3.save(chunk, padding=0)
					# Send the modified chunk to the client
					self.wfile.write(chunk.getvalue())
				else:
					# Send the unmodified chunk to the client
					self.wfile.write(chunk)

def run_server():
	# Set up the server
	server_address = ('', 8000)
	httpd = HTTPServer(server_address, MyRequestHandler)

	# Start the server
	print('Starting server...')
	httpd.serve_forever()

if __name__ == '__main__':
	run_server()