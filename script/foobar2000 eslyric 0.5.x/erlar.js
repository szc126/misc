export function getConfig(cfg) {
	cfg.name = 'erlar.ru (Татар җырлары)';
	cfg.version = '2026.07.09';
	cfg.author = '極度良好（です）';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	// 相關文件夾外則取消搜索
	// skip songs that aren't in my "Tatar music" folder
	// 特定フォルダー外のものを無視
	//
	// ☞ 量體裁衣
	// ☞ modify as needed
	// ☞ 自身の状況に応じて修正をしましょう
	//
	if (meta.path.indexOf('韃') == -1) {
		console.log('範圍外，已跳過／Skipped: Out of scope');
		return;
	}

	let headers = {
		'User-Agent': 'erlar.ru for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 5;

	request({
		url: 'https://erlar.ru/search/node/' + encodeURIComponent(meta.title),
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		if (body.indexOf('По вашему запросу ничего не найдено') > 1) {
			return;
		}

		let items = body.match(/(?<=")https:\/\/erlar\.ru\/node\/\d+(?=")/g) || [];
		for (let i_item = 0; i_item < Math.min(items.length, N_LYRICS_MAX); i_item++) {
			request({
				url: items[i_item],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				const lyricMeta = man.createLyric();

				lyricMeta.title = body.match(/<title>([^|]+) \| /)[1];
				const paren = lyricMeta.title.match(/^(.+) (\(.+ вариант\))$/);
				if (paren) {
					lyricMeta.title = paren[1];
					lyricMeta.album = paren[2];
				}

				let lyric = body.match(/(?<=<p class="line_[a-z]+">)(.+?)(?=<\/p>)/gs);
				lyric = lyric.join('\n\n');
				lyric = lyric
					.replace(/<br \/>/g, '')
				;
				lyricMeta.lyricText = lyric;

				// use ESLyric artist matching
				const artists = body.match(/(?<=<div id="artist">).+(?=<.div>)/);
				if (artists) {
					for (const match of artists[0].matchAll(/"">(.+?)<.a/g)) {
						const lyricMetaNew = man.createLyric();
						lyricMetaNew.title = lyricMeta.title;
						lyricMetaNew.album = lyricMeta.album;
						lyricMetaNew.artist = match[1];
						// circumvent deduplication
						lyricMetaNew.lyricText = '[ar:' + lyricMetaNew.artist + ']\n\n' + lyricMeta.lyricText;
						man.addLyric(lyricMetaNew);
					}
				} else {
					man.addLyric(lyricMeta);
				}
			});
		}
	});
}