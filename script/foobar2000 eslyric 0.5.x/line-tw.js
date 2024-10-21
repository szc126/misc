export function getConfig(cfg) {
	cfg.name = 'LINE MUSIC Taiwan';
	cfg.version = '2024.09.28';
	cfg.author = 'demigirl eggbug';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'CHANNEL-ID': 1581655766,
		'User-Agent': 'LINE for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 3;

	request({
		url: 'https://music-tw.line.me/api/search/v4/track.json?query=' + encodeURIComponent(meta.title) + '&start=1&display=' + N_LYRICS_MAX + '&sort=RELEVANCE',
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

			lyricMeta.lyricText = result['lyrics'];
			man.addLyric(lyricMeta);
		}
	});
}