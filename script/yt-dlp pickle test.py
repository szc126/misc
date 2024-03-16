#!/usr/bin/env python3

import yt_dlp
from diskcache import Cache

with yt_dlp.YoutubeDL({'simulate': True}) as ytdl:
	for url in ['https://www.youtube.com/watch?v=aqz-KE-bpKQ']:
		cache = Cache('/tmp/cache-foo')
		info = cache.memoize()(ytdl.extract_info)(url)
		print(info['title'], info['id'])
