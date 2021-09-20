#!/usr/bin/env python3

# firefox > network > export to har
# with a filter, only the results are exported

# > a.py *.har

import sys
import json
from haralyzer import HarParser, HarPage
import pprint
from subprocess import call # https://unix.stackexchange.com/a/238185
from subprocess import run # https://docs.python.org/ja/3/library/subprocess.html#subprocess.call

pp = pprint.PrettyPrinter(indent = 1)
pprint = pp.pprint

with open(sys.argv[1], 'r') as file:
	har_parser = HarParser(json.loads(file.read()))
	for har_page in har_parser.pages:
		for har_entry in har_page.entries:
			entries_raw = []
			entries_flat = []

			if 'Likes?' in har_entry.url or 'UserMedia?' in har_entry.url:
				entries_raw = json.loads(har_entry.response.text)['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']
			elif 'TweetDetail?' in har_entry.url:
				entries_raw = json.loads(har_entry.response.text)['data']['threaded_conversation_with_injections']['instructions'][0]['entries']

			for entry in entries_raw:
				if entry['content']['entryType'] == 'TimelineTimelineItem':
					item_content = entry['content']['itemContent']
					if item_content['itemType'] == 'TimelineTweet':
						entries_flat.append(item_content)
				elif entry['content']['entryType'] == 'TimelineTimelineModule':
					for item in entry['content']['items']:
						item_content = item['item']['itemContent']
						if item_content['itemType'] == 'TimelineTweet':
							entries_flat.append(item_content)

			for entry in entries_flat:
				poster = entry['tweet_results']['result']['core']['user_results']['result']['legacy']
				name = poster['name']
				screen_name = poster['screen_name']

				full_text = entry['tweet_results']['result']['legacy']['full_text']
				id_str = entry['tweet_results']['result']['legacy']['id_str']

				url = f'https://twitter.com/{screen_name}/status/{id_str}'

				fs_safe = f'{screen_name}-status-{id_str}'

				media = False
				if 'extended_entities' in entry['tweet_results']['result']['legacy']:
					medias = entry['tweet_results']['result']['legacy']['extended_entities']['media']
					#with open('.indices.txt', 'a') as file_indices:
					for i, media in enumerate(medias):
						pprint(media)
						if 'video_thumb' in media['media_url_https']:
							#pass
							variants = [variant for variant in media['video_info']['variants'] if variant['content_type'] != 'application/x-mpegURL']
							variants.sort(key = lambda variant: variant['bitrate'])

							url = variants[-1]['url']
							bitrate = variants[-1]['bitrate']
							ext = url.split('.')[-1].split('?')[0]
							run(f'wget "{url}" -O "{fs_safe}-{i+1} (bitrate {bitrate}).{ext}"', shell = True, check = 1)
						else:
							#image_id = media['media_url_https'].split('/')[4].split('.')[0]
							#file_indices.write(f'{image_id} {i+1}\n')
							url = media['media_url_https']
							ext = url.split('.')[-1]
							run(f'wget "{url}" -O "{fs_safe}-{i+1}.{ext}"', shell = True, check = 1)

				print('\t', '----')
				print('\t', name, '\t', url)
				print(full_text)
				print()

				#call(f'you-get {url} --output-dir {fs_safe}', shell = True)
				with open(f'{fs_safe}.txt', 'w') as t:
					t.write(full_text)

