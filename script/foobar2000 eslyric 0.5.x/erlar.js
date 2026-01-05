export function getConfig(cfg) {
	cfg.name = 'erlar.ru (Татар җырлары)';
	cfg.version = '2025.11.25';
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
			let lyricMeta = man.createLyric();

			request({
				url: items[i_item],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				lyricMeta.title = body.match(/<title>([^|]+) \| /)[1];

				let paren = lyricMeta.title.match(/ \(.+ вариант\)/);
				lyricMeta.artist = paren ? paren[0].slice(1) : '';
				lyricMeta.title = lyricMeta.title.slice(0, -1 * (lyricMeta.artist.length));

				let lyric = body.match(/(?<=<p class="line_[a-z]+">)(.+?)(?=<\/p>)/gs);
				lyric = lyric.join('\n\n');
				lyric = lyric
					.replace(/<br \/>/g, '')
				;

				lyricMeta.lyricText = lyric;
				man.addLyric(lyricMeta);
			});
		}
	});
}