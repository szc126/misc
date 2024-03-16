#!/usr/bin/env python

import sys

lines = [ [] for _ in range(int(sys.argv[1])) ]
set = 0
while True:
	line = input()
	if line:
		lines[set].append(line)
	else:
		set += 1
	if set > len(lines):
		break

max_len = max([len(set) for set in lines])
for i in range(len(lines)):
	while len(lines[i]) < max_len:
		lines[i].append('')

if len(lines) == 4:
	a = zip(lines[0], lines[1])
	b = zip(lines[2], lines[3])

	a = [';' + yue + ':' + cmn for yue, cmn in a]
	b = [';' + yue + ':' + cmn for yue, cmn in b]

	print('\n'.join('\n'.join(ab) for ab in zip(a, b)))

if len(lines) == 2:
	lines = list(zip(*lines))
	lines = ['\n'.join(line) for line in lines]
	lines = '\n'.join(lines)

	print(lines)