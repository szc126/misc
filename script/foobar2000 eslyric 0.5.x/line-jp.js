export function getConfig(cfg) {
	cfg.name = 'LINE MUSIC Japan';
	cfg.version = '2024.09.28';
	cfg.author = 'demiboy eggbug';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': 'LINE for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 3;

	request({
		url: 'https://music.line.me/api2/search/tracks.v1?query=' + encodeURIComponent(meta.title + ' ' + meta.artist) + '&start=1&display=' + N_LYRICS_MAX + '&sort=RELEVANCE',
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		body = JSON.parse(body);
		for (let i_item = 0; i_item < Math.min(body['response']['result']['tracks'].length, N_LYRICS_MAX); i_item++) {
			let result = body['response']['result']['tracks'][i_item];
			let lyricMeta = man.createLyric();

			if (!result['hasLyric']) {
				break;
			}

			lyricMeta.album = result['album']['albumTitle'];
			lyricMeta.artist = result['artists'][0]['artistName'];
			lyricMeta.title = result['trackTitle'];

			request({
				url: 'https://music.line.me/api2/track/' + result['trackId'] + '/lyrics.v1?nonSync=true',
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				body = JSON.parse(body);

				lyricMeta.lyricText = body['response']['result']['lyric']['lyric'];
				man.addLyric(lyricMeta);
			});
		}
	});
}