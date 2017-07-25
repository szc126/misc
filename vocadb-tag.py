import argparse
import colorama
import json
import mutagen
import re
import requests

LANGUAGE = 'Default' # Default, Japanese, Romaji, English

METADATA_FORMAT = {
	'TITLE': '$title',
	'ARTIST': '$vocalists',
	'COMPOSER': '$producers',
	'ALBUM': 'foobar-album',
	'GENRE': 'foobar-genre',
	'DATE': '$year',
	'URL': '$url',
	'COMMENT': '$producers feat. $vocalists ; $song_type song ; $vocadb_id@VocaDB',
}

service_regexes = {
	'NicoNicoDouga': '[sn]m\d+',
	'Youtube': '[A-Za-z0-9_-]{11}'
}

service_urls = {
	'NicoNicoDouga': 'http://www.nicovideo.jp/watch/{}',
	'Youtube': 'https://www.youtube.com/watch?v={}'
}

vocadb_api_request_url = 'https://vocadb.net/api/songs/byPv?pvService={}&pvId={}&fields=Artists&lang={}'

parser = argparse.ArgumentParser(description='LOREM IPSUM DOLOR SIT AMET')
parser.add_argument('FOOBAR', help='LOREM IPSUM DOLOR SIT AMET', metavar='LOREM IPSUM DOLOR SIT AMET')
args = parser.parse_args()

def fetch_data(service, id):
	"""Fetch PV data from the VocaDB API"""

	return requests.get(vocadb_api_request_url.format(service, id, LANGUAGE))

def check_connectivity():
	"""Check to see if the NND API can be reached"""

	try:
		fetch_data('NicoNicoDouga', 'sm26661454')
	except:
		print(colorama.Back.RED + 'Server could not be reached!')
		quit()

def generate_metadata(service, id):
	"""Parse and rearrange the data from the VocaDB API"""

	api_data = fetch_data(service, id)

	if api_data.content == b'null':
		raise Exception(f'The video \'{id}@{service}\' is not registered on VocaDB!')

	api_data = json.loads(api_data.content)

	metadata = {
		'vocadb_id': None,
		'title': None,
		'song_type': None,
		'publish_date': None, 'year': None,
		'producers': [],
		'vocalists': [],
		'x_synthesizers': {
			'vocaloid': None,
			'utau': None,
			'cevio': None,
			'other_synthesizer': None,
			'actual_human_people': None,
		},
		'url': [],
	}

	metadata['vocadb_id'] = api_data['id']

	metadata['title'] = api_data['name']

	metadata['song_type'] = api_data['songType']

	metadata['publish_date'] = api_data['publishDate']

	metadata['year'] = metadata['publish_date'][0:4] # it just werks

	for artist in api_data['artists']:
		# print(artist)
		# print()

		if artist['artist']['artistType'] == 'Vocaloid':
			metadata['x_synthesizers']['vocaloid'] = True
			metadata['vocalists'].append(artist['name'])
		elif artist['artist']['artistType'] == 'UTAU':
			metadata['x_synthesizers']['utau'] = True
			metadata['vocalists'].append(artist['name'])
		elif artist['artist']['artistType'] == 'CeVIO':
			metadata['x_synthesizers']['cevio'] = True
			metadata['vocalists'].append(artist['name'])
		elif artist['artist']['artistType'] == 'OtherVoiceSynthesizer':
			metadata['x_synthesizers']['other_synthesizer'] = True
			metadata['vocalists'].append(artist['name'])
		elif 'Vocalist' in artist['roles']: # what's the difference between 'roles' and 'effectiveRoles'
			metadata['x_synthesizers']['actual_human_people'] = True
			metadata['vocalists'].append(artist['name'])

		elif 'Composer' in artist['roles']:
			metadata['producers'].append(artist['name'])

		elif 'Default' in artist['roles'] and 'Producer' in artist['categories']:
			metadata['producers'].append(artist['name'])

	metadata['url'] = service_urls[service].format(id)

	return metadata

def determine_service_and_id(path):
	"""Test path against regexes to determine the service and PV ID"""

	for service in service_regexes:
		matches = re.search('({})'.format(service_regexes[service]) + '.+(mp3|m4a)', path)

		if matches:
			return service, matches.group(1)
			break
		else:
			print(f'tis not {service}')

def tag_file(path):
	"""Given the file path, tag the file"""

	service, id = determine_service_and_id(path)
	metadata = generate_metadata(service, id)

	# NOT WORKING

	audio =  mutagen.easyid3.EasyID3(path)
	print(audio)

	def metadata_returner(x):
		metadata_value = metadata[x.group(1)]
		if type(metadata_value) is list:
			metadata_value = '; '.join(metadata_value)
		elif type(metadata_value) is int:
			metadata_value = str(metadata_value)
		return metadata_value

	for field in METADATA_FORMAT:
		metadata_value = re.sub('\$([a-z_]+)', metadata_returner, METADATA_FORMAT[field])
		print(field, metadata_value)
		audio[field] = metadata_value

	audio.pprint()
	audio.save()

def main():
	check_connectivity()

	path = args.FOOBAR

	tag_file(path)

if __name__ == "__main__":
	main()