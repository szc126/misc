import logging
import math
import os
import re
import requests
import shutil
import time

URL_BASE = 'http://dl.ndl.go.jp/view/jpegOutput?itemId=info%3Andljp%2Fpid%2F1126379&contentNo={0}&outputScale=1'
FILE_EXTENSION = 'jpg'
PAGE_INITIAL = 1
PAGE_FINAL = 425
INCREMENT_PADDING = 0 # not yet used
REFERRER = '' # not yet used
COOLDOWN_LENGTH = 60

is_cooldown = False
auto_cooldown_counter = 1
auto_cooldown_length = 5

elapsed_start = 0
elapsed_end = 0
elapsed_final = 0

# https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests

def configure_logging():
	LOG_FILENAME = 'log image dl.log'

	logging.basicConfig(
		level = logging.INFO,
		format = '%(message)s',
	)

def start_timer():
	global elapsed_start

	elapsed_start = time.time()

def end_timer():
	elapsed_end = time.time()
	elapsed_final = elapsed_end - elapsed_start
	print('Finished in {0} seconds.'.format(int(elapsed_final)))
	print()

def try_sleeping(i):
	print('Sleeping for {0} seconds...'.format(COOLDOWN_LENGTH))
	time.sleep(COOLDOWN_LENGTH)

def try_auto_sleeping():
	global auto_cooldown_length
	global auto_cooldown_counter

	auto_cooldown_length = 20 * math.log(auto_cooldown_counter * 2)
	auto_cooldown_counter += 1

	print('Sleeping for {0} seconds (#{1})...'.format(int(auto_cooldown_length), auto_cooldown_counter))
	time.sleep(auto_cooldown_length)

def get_response(i):
	print('Retrieving item {0} of {1}.'.format(i, PAGE_FINAL))
	url = URL_BASE.format(i)
	response = requests.get(url, stream=True)

	return response

def save_response(i, response, filename):
	with open(filename, 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response
	print('Saved.')

def main():
	times = []

	configure_logging()

	for i in range(PAGE_INITIAL, PAGE_FINAL + 1):
		filename = '{0}.{1}'.format(i, FILE_EXTENSION)

		if not os.path.isfile(filename):
			start_timer()

			while True:
				response = get_response(i)

				if response.status_code == 200:
					save_response(i, response, filename)

					end_timer()

					break
				else:
					print('Failed ({0}).'.format(response.status_code))

					# try_auto_sleeping()
					try_sleeping(i)

if __name__ == "__main__":
	main()