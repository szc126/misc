export function getConfig(cfg) {
	cfg.name = 'LyricsTranslate.com';
	cfg.version = '2026.04.20';
	cfg.author = 'ik kom van de straat';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': 'LyricsTranslate.com for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 5;

	request({
		url: 'https://lyricstranslate.com/en/songs/0/' + encodeURIComponent(meta.artist || 'none') + '/' + encodeURIComponent(meta.title || 'none'),
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		if (body.indexOf('lyricstranslatesearchnoresults') > 1) {
			return;
		}

		let items = body.match(/(?<=a href=")\/en\/.+?-lyrics.html(?=")/g) || [];
		for (let i_item = 0; i_item < Math.min(items.length, N_LYRICS_MAX); i_item++) {
			let lyricMeta = man.createLyric();

			request({
				url: 'https://lyricstranslate.com' + items[i_item],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				lyricMeta.artist = body.match(/artist: "(.+)"/)[1];
				lyricMeta.title = body.match(/song: "(.+)"/)[1];

				if (body.indexOf('video-with-subtitles') > 1) {
					let nid = body.match(/nid="(.+?)"/)[1];
					let youtube = body.match(/youtube="(.+?)"/)[1];

					request({
						url: 'https://lyricstranslate.com/en/callback/subtitles/' + nid + '/' + youtube,
						headers: headers,
					}, (err, res, body) => {
						if (err || res.statusCode != 200) {
							return;
						}

						body = JSON.parse(body);

						lyricMeta.fileType = 'vtt';
						lyricMeta.lyricText = body['webtvv'];
						man.addLyric(lyricMeta);
					});
				} else {
					let lyric = body.match(/(?<=<div class=['"](?:ll-\d+-\d+|emptyline)['"]>\n?).+?(?=<.div>)/g);
					lyric = lyric.join('\n');
					lyric = lyric
						.replace(/&nbsp;/g, '')
					;

					lyricMeta.lyricText = lyric;
					man.addLyric(lyricMeta);
				}
			});
		}
	});
}