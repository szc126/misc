#!/usr/bin/env python
import sys
import datetime
with open(sys.argv[1], 'r') as f:
	current = datetime.timedelta()
	for line in f.readlines():
		t, ttext = line.split('\t')
		tm, ts = t.split(':')
		d = datetime.timedelta(minutes=float(tm), seconds=float(ts))
		match sys.argv[2]:
			case 'h':
				print(str(current) + '\t' + ttext.strip())
			case 'm':
				th, tm, ts = str(current).split(':')
				print(str(int(th) * 60 + int(tm)) + ':' + str(ts) + '\t' + ttext.strip())
		current += d