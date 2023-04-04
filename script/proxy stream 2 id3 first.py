#!/usr/bin/env python

# authored by ChatGPT

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

		audio_data = BytesIO()
		audio = ID3()
		audio.add(TIT2(encoding=3, text=title))
		audio.add(TPE1(encoding=3, text=artist))
		audio.add(TALB(encoding=3, text=album))
		audio.save(audio_data)
		audio_data.seek(0)
		self.send_response(200)
		self.send_header('Content-type', 'audio/mpeg')
		self.send_header('Content-Length', response.headers.get('Content-Length'))
		self.end_headers()
		self.wfile.write(audio_data.getvalue())
		for chunk in response.iter_content(chunk_size=1024):
			if chunk:
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