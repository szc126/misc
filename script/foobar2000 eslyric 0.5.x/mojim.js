export function getConfig(cfg) {
	cfg.name = '魔鏡';
	cfg.version = '2023.04.08';
	cfg.author = 'transgender amen break';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': '魔鏡 for ESLyric for foobar2000',
	};
	let url = 'https://mojim.com/' + encodeURIComponent(meta.title) + '.html?t3';

	request({
		url: url,
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		let items = body.match(/<dd [\S\s]+?<.dd>/g);
		for (let i_item = 1; i_item < items.length; i_item++) {
			let lrc_meta_raw = items[i_item].match(/.+mxsh_ss.+/g);
			let lyricMeta = man.createLyric();

			lyricMeta.artist = lrc_meta_raw[1].match(/<a .+>(.+)<.a>/)[1];
			lyricMeta.album = lrc_meta_raw[2].match(/<a .+>(.+)<.a>/)[1];
			lyricMeta.title = lrc_meta_raw[3].replace(/<font [^<>]+>|<.font>/g, '').match(/<a .+>(.+)<.a>/)[1].replace(/^[0-9]+\./, '');

			// discard partial title match
			// to avoid downloading 200 irrelevant webpages
			// note that parentheses etc are ignored in search results
			//if (!lrc_meta_raw[3].match(/[0-9].\<font.+<.font><.a>/)) {
			if (lyricMeta.title.replace(/[\s()+-]/g, '').toLowerCase() != meta.title.replace(/[\s()+-]/g, '').toLowerCase()) {
				console.log('Skipped: ' + lyricMeta.artist + '／' + lyricMeta.title);
				continue;
			}

			request({
				url: 'https://mojim.com/' + lrc_meta_raw[3].match(/<a href="([^"]+)"/)[1],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				let lyric = body.match(/<dl id=.fsZx1. [\S\s]+?<.dl>/)[0];
				lyric = lyric
					.replace(/&#([0-9]+)/g, function(_, dec) {
						return String.fromCodePoint(dec);
					})
					.replace(/<br.*?>/g, '\n')
					.replace(/.+Mojim.+\n/g, '')
					.replace(/^[\S\s]+<.dt>\n+[^\n]+\n+/, '') // /[^\n]+\n+/ is song title + \n\n
					.replace(/\n+<ol>[\S\s]+/, '')
				;

				lyric = lyric
					// 將[by:user]和[00:00.00]黐埋一齊
					.replace(/(\[[a-z]+:.*?\])\n+(\[[0-9:.]{8}\])/g, '$1\n$2')
					// 以[]分割
					.replace(/\n\n(?=\[.*?\])/g, '\n\n--------\n\n')
				;
				lyric = lyric.split(/\n-{8,}\n/g);

				for (let i_lyric = 0; i_lyric < lyric.length; i_lyric++) {
					lyricMeta.lyricText = lyric[i_lyric].trim();
					man.addLyric(lyricMeta);
				}
			});
		}
	});
}