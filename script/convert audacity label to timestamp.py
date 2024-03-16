#!/usr/bin/env python
import sys
import datetime
with open(sys.argv[1], 'r') as f:
	for line in f.readlines():
		ta, tb, ttext = line.split('\t')
		tstamp = datetime.timedelta(seconds=float(ta))
		print(str(tstamp)[2:2+5],ttext.strip())