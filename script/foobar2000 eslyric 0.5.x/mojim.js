export function getConfig(cfg) {
	cfg.name = '魔鏡';
	cfg.version = '2023.05.30';
	cfg.author = 'transgender amen break';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': '魔鏡 for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 5;

	let ids_artist = man.getSvcData('mojim ' + meta.artist);
	if (!ids_artist) {
		request({
			url: 'https://mojim.com/' + encodeURIComponent(meta.artist) + '.html?t1',
			headers: headers,
		}, (err, res, body) => {
			if (err || res.statusCode != 200) {
				return;
			}

			ids_artist = body.match(/twh\d+\.htm/g) || [];
			man.setSvcData('mojim ' + meta.artist, ids_artist);
		});
	} else {
		// getSvcData returns string
		ids_artist = ids_artist.split(',');
	}

	request({
		url: 'https://mojim.com/' + encodeURIComponent(meta.title) + '.html?t3',
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		let items = body.match(/<dd [\S\s]+?<.dd>/g) || [];
		for (let i_item = 1; i_item < items.length; i_item++) {
			let lrc_meta_raw = items[i_item].match(/.+mxsh_ss.+/g);
			let lyricMeta = man.createLyric();

			// discard artist mismatch
			let artist_match = false;
			if (ids_artist.length == 0) {
				// download all lyrics
				artist_match = true;

				// do not download 100 lyrics
				if (i_item > N_LYRICS_MAX) {
					continue;
				}
			} else {
				// download lyrics with a matching artist
				for (let i_id = 0; i_id < ids_artist.length; i_id++) {
					if (lrc_meta_raw[1].indexOf(ids_artist[i_id]) > -1) {
						artist_match = true;
					}
				}
			}

			lyricMeta.artist = lrc_meta_raw[1].match(/<a .+>(.+)<.a>/)[1];
			lyricMeta.album = lrc_meta_raw[2].match(/<a .+>(.+)<.a>/)[1];
			lyricMeta.title = lrc_meta_raw[3].replace(/<font [^<>]+>|<.font>/g, '').match(/<a .+>(.+)<.a>/)[1].replace(/^[0-9]+\./, '');

			// discard artist mismatch
			if (!artist_match) {
				console.log('Skipped: ' + lyricMeta.artist + '／' + lyricMeta.title);
				continue;
			}

			// discard partial title match
			// to avoid downloading 200 irrelevant webpages
			// note that parentheses etc are ignored in search results
			/*
			//if (!lrc_meta_raw[3].match(/[0-9].\<font.+<.font><.a>/)) {
			if (lyricMeta.title.replace(/[\s()+-]/g, '').toLowerCase() != meta.title.replace(/[\s()+-]/g, '').toLowerCase()) {
				console.log('Skipped: ' + lyricMeta.artist + '／' + lyricMeta.title);
				continue;
			}
			*/

			let id_song = lrc_meta_raw[3].match(/twy[a-z0-9]+\.htm/g);
			request({
				url: 'https://mojim.com/' + id_song,
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