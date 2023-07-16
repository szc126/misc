export function getConfig(cfg) {
	cfg.name = '벅스 Bugs!';
	cfg.version = '2023.06.28';
	cfg.author = 'cisgender(derogatory) exclamation mark';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': '벅스 for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 2;

	request({
		url: 'https://music.bugs.co.kr/search/track?sort=P&q=' + encodeURIComponent(meta.title + ' ' + meta.artist),
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		let urls = body.match(/(?<=href=")[^"]+\/track\/[^"]+(?=")/g) || [];
		for (let i_url = 0; i_url < Math.min(urls.length, N_LYRICS_MAX); i_url++) {
			request({
				url: urls[i_url],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				if (body.indexOf('<xmp>') < 0) {
					return;
				}

				let lyricMeta = man.createLyric();
				lyricMeta.title = body.match(/property="sc:track_title" content="(.+)"/)[1];
				lyricMeta.artist = body.match(/property="sc:artist_nm" content="(.+)"/)[1];
				lyricMeta.album = body.match(/property="sc:album_title" content="(.+)"/)[1];
				lyricMeta.lyricText = body.match(/<xmp>([\S\s]+?)<.xmp>/)[1];
				man.addLyric(lyricMeta);
			});
		}
	});
}