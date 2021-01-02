#!/usr/bin/env python3

from disk_cache_decorator import disk_cache_decorator
import random

def a(text):
	return text[::-1] + ' ' + str(random.randrange(1, 400))

@disk_cache_decorator('te_de.pickle')
def a_de(text):
	return text[::-1] + ' ' + str(random.randrange(1, 400))

print(
	a('Wikipedia the free encyclopedia')
)
print(
	disk_cache_decorator('te.pickle')(a)('Fireflies by owl city')
)
print(
	a_de('Lorem ipsum dolor')
)

a = disk_cache_decorator('te.pickle')(a)

print(
	a('Republic of Korea')
)