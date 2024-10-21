export function getConfig(cfg) {
	cfg.name = 'KKBOX';
	cfg.version = '2024.09.28';
	cfg.author = 'tragic old man yaoi';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': 'KKBOX for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 2;

	request({
		url: 'https://www.kkbox.com/api/search/song?q=' + encodeURIComponent(meta.title + ' ' + meta.artist) + '&terr=tw&lang=tc',
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		body = JSON.parse(body);
		for (let i_item = 0; i_item < Math.min(body['data']['result'].length, N_LYRICS_MAX); i_item++) {
			let result = body['data']['result'][i_item];
			let lyricMeta = man.createLyric();

			if (!result['has_lyrics']) {
				break;
			}

			lyricMeta.title = result['name'];
			lyricMeta.album = result['album']['name'];
			lyricMeta.artist = result['artist_roles'].map(artist => artist.name).join(', ');

			request({
				url: result['url'],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				let lyric = body.match(/(?<=<p>).+(?=<.p>)/s)[0];
				lyric = lyric
					.replace(/&#([0-9]+);/g, function(_, dec) {
						return String.fromCodePoint(dec);
					})
					.replace(/\n|\r|<p>|<.p>/g, '')
					.replace(/&nbsp;/g, ' ')
					.replace(/<br .>|<br>/g, '\n')
				;

				lyricMeta.lyricText = lyric;
				man.addLyric(lyricMeta);
			});
		}
	});
}