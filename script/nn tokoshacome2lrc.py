#!/usr/bin/env python
import sys, json
with open(sys.argv[1], 'r') as file:
	data = json.load(file)
by = False
for c in data['data']['threads'][0]['comments']:
	if not by:
		print('[by:投稿者コメント]')
		by = True
	s, ms = divmod(c['vposMs'], 1000)
	m, s = divmod(s, 60)
	ms = ms//10
	m, s, ms = str(m).zfill(2), str(s).zfill(2), str(ms).zfill(2)
	print(f'[{m}:{s}.{ms}]' + c['body'])