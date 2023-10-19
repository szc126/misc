#!/usr/bin/env python

lines = [[], []]
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

lines = list(zip(*lines))
lines = ['\n'.join(line) for line in lines]
lines = '\n'.join(lines)

print(lines)