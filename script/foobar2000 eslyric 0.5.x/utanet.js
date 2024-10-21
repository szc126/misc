export function getConfig(cfg) {
	cfg.name = '歌ネット';
	cfg.version = '2024.09.28';
	cfg.author = 'bratya karamazovy autumn';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': '歌ネット for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 2;

	request({
		url: 'https://www.uta-net.com/search/?Keyword=' + encodeURIComponent(meta.title) + '&Aselect=2&Bselect=3',
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		if (body.indexOf('該当する歌詞はございません') > 1) {
			return;
		}

		let items = body.match(/(?<=href=").song.[0-9]+.(?=" class=)/g);
		for (let i_item = 0; i_item < Math.min(items.length, N_LYRICS_MAX); i_item++) {
			let lyricMeta = man.createLyric();

			request({
				url: 'https://www.uta-net.com' + items[i_item],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				let meta = body.match(/content="([^"]+)の「([^"]+)」歌詞ページ/);
				lyricMeta.artist = meta[1];
				lyricMeta.title = meta[2];

				let lyric = body.match(/(?<=<div id="kashi_area" itemprop="text">).+?(?=<.div>)/)[0];
				lyric = lyric
					.replace(/<br \/>/g, '\n')
				;

				console.log(lyric);
				lyricMeta.lyricText = lyric;
				man.addLyric(lyricMeta);
			});
		}
	});
}