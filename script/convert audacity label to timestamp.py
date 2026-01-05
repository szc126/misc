#!/usr/bin/env python
import sys
import datetime
with open(sys.argv[1], 'r') as f:
	for line in f.readlines():
		ta, tb, ttext = line.split('\t')
		d = str(datetime.timedelta(seconds=float(ta)))
		d = d + '.000000' if not '.' in d else d
		match sys.argv[2]:
			case 'cue':
				print(str(d)[2:2+8].replace('.', ':') + '\t' + ttext.strip())
			case 'lrc':
				print(str(d)[2:2+8] + '\t' + ttext.strip())
			case 'vtt':
				print(str(d)[2:2+9] + '\t' + ttext.strip())