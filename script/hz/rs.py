import re

radicals =  [
	'',
	'⼀', '⼁', '⼂', '⼃', '⼄', '⼅',
	'⼆', '⼇', '⼈', '⼉', '⼊', '⼋', '⼌', '⼍', '⼎', '⼏', '⼐', '⼑', '⼒', '⼓', '⼔', '⼕', '⼖', '⼗', '⼘', '⼙', '⼚', '⼛', '⼜',
	'⼝', '⼞', '⼟', '⼠', '⼡', '⼢', '⼣', '⼤', '⼥', '⼦', '⼧', '⼨', '⼩', '⼪', '⼫', '⼬', '⼭', '⼮', '⼯', '⼰', '⼱', '⼲', '⼳', '⼴', '⼵', '⼶', '⼷', '⼸', '⼹', '⼺', '⼻',
	'⼼', '⼽', '⼾', '⼿', '⽀', '⽁', '⽂', '⽃', '⽄', '⽅', '⽆', '⽇', '⽈', '⽉', '⽊', '⽋', '⽌', '⽍', '⽎', '⽏', '⽐', '⽑', '⽒', '⽓', '⽔', '⽕', '⽖', '⽗', '⽘', '⽙', '⽚', '⽛', '⽜', '⽝',
	'⽞', '⽟', '⽠', '⽡', '⽢', '⽣', '⽤', '⽥', '⽦', '⽧', '⽨', '⽩', '⽪', '⽫', '⽬', '⽭', '⽮', '⽯', '⽰', '⽱', '⽲', '⽳', '⽴',
	'⽵', '⽶', '⽷', '⽸', '⽹', '⽺', '⽻', '⽼', '⽽', '⽾', '⽿', '⾀', '⾁', '⾂', '⾃', '⾄', '⾅', '⾆', '⾇', '⾈', '⾉', '⾊', '⾋', '⾌', '⾍', '⾎', '⾏', '⾐', '⾑',
	'⾒', '⾓', '⾔', '⾕', '⾖', '⾗', '⾘', '⾙', '⾚', '⾛', '⾜', '⾝', '⾞', '⾟', '⾠', '⾡', '⾢', '⾣', '⾤', '⾥',
	'⾦', '⾧', '⾨', '⾩', '⾪', '⾫', '⾬', '⾭', '⾮',
	'⾯', '⾰', '⾱', '⾲', '⾳', '⾴', '⾵', '⾶', '⾷', '⾸', '⾹',
	'⾺', '⾻', '⾼', '⾽', '⾾', '⾿', '⿀', '⿁',
	'⿂', '⿃', '⿄', '⿅', '⿆', '⿇',
	'⿈', '⿉', '⿊', '⿋',
	'⿌', '⿍', '⿎', '⿏',
	'⿐', '⿑',
	'⿒',
	'⿓', '⿔',
	'⿕',
]

simplified_radical = {
	'⽙': '⺦',
	'⽷': '⺰',
	'⾒': '⻅',
	'⾔': '⻈',
	'⾙': '⻉',
	'⾞': '⻋',
	'⾡': '⻌', # i guess?
	'⾦': '⻐',
	'⾧': '⻓',
	'⾨': '⻔',
	'⾱': '⻙',
	'⾴': '⻚',
	'⾵': '⻛',
	'⾶': '⻜',
	'⾷': '⻠',
	'⾺': '⻢',
	'⿂': '⻥',
	'⿃': '⻦',
	'⿄': '⻧',
	'⿆': '⻨',
	'⿈': '⻩',
	'⿌': '⻪',
	'⿑': '⻬',
	'⿒': '⻮',
	'⿓': '⻰',
	'⿔': '⻳',
}

def rs_conv(rs):
	rs_set_out = []

	for rs in rs_set:
		rad, _, stk = rs.partition('.')

		simplified = False

		if ('\'' in rad):
			simplified = True
			rad = rad.replace('\'', '')

		rad = radicals[int(rad)] # convert number to hanzi

		if simplified:
			rad = simplified_radical[rad]

		stk = stk.zfill(2) # pad stroke number to two digits

		rs_set_out.append(rad + stk)

	return rs_set_out

# filename = 'Unihan_RadicalStrokeCounts.txt'
filename = 'Unihan_IRGSources.txt'

rs_all = dict()

date = ''

with open(f'../Unicode/Unihan/{filename}', mode='r', encoding='utf-8') as file:
	for line in file:
		matches = re.search('U\+(.+)\tkRSUnicode\t(.+)', line)

		if (matches):
			hex, rs = matches.group(1), matches.group(2)

			hex = int(f'0x{hex}', 16) # convert hex to decimal

			if (int(0xf900) <= hex <= int(0xfaff)) or (int(0x2f800) <= hex <= int(0x2fa1f)):
				pass # cjk compatibility ideographs
			else:
				char = chr(hex) # convert codepoint to hanzi

				rs_set = [rs]

				if (' ' in rs_set[0]):
					a, _, c = rs.partition(' ') # why can't i do rs_set[0], _, rs_set[1]
					rs_set[0] = a
					rs_set.append(c)

				rs_set = rs_conv(rs_set) # process the 000.00 format

				rs_all[char] = rs_set
		elif ('Date' in line):
			date = line

with open(f'out-rs.txt', mode='w', encoding='utf-8') as file:
	for char in rs_all:
		file.write(f'{char}\t' + '\t'.join(rs_all[char]) + '\n')

with open(f'out-rs-wt.txt', mode='w', encoding='utf-8') as file:
	file.write(date.replace('#', f'-- {filename};'))
	file.write('' + '\n')
	file.write('local export = {}' + '\n')
	file.write('' + '\n')
	file.write('export.skeys = {')

	last_radical = ''

	for char in rs_all:
		rs = rs_all[char][0] # dispose of secondary index

		if last_radical != rs[0]:
			file.write('\n')

		last_radical = rs[0]

		file.write(f'\t[\'{char}\']=\'{rs}\',')

	file.write('\n' + '};' + '\n')
	file.write('' + '\n')
	file.write('return export')