export function getConfig(cfg) {
	cfg.name = 'Eurobeat-Prime';
	cfg.version = '2023.06.07';
	cfg.author = 'parapara bara boys';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	// 相關文件夾外則取消搜索
	// skip songs that aren't in my eurobeat folder
	// 特定フォルダー外のものを無視
	//
	// ☞ 量體裁衣
	// ☞ modify as needed
	// ☞ 自身の状況に応じて修正をしましょう
	//
	if (meta.path.indexOf('eurobeat') == -1) {
		console.log('範圍外，已跳過／Skipped: Out of scope');
		return;
	}

	let headers = {
		'User-Agent': 'Eurobeat-Prime for ESLyric for foobar2000',
	};
	const artist_initial = meta.artist[0].toLowerCase();

	let songs_list = man.getSvcData('eurobeat-prime ' + artist_initial);
	if (!songs_list) {
		request({
			url: 'https://www.eurobeat-prime.com/lyrics.php?artist=' + artist_initial,
			headers: headers,
		}, (err, res, body) => {
			if (err || res.statusCode != 200) {
				return;
			}

			songs_list = body;
			man.setSvcData('eurobeat-prime ' + artist_initial, body);
		});
	}

	const song_search_regex = new RegExp('([^<>\n]+) - <a (.+)>(' + meta.title.replace(/'/g, '&#039;') + ')<.a>', 'gi');
	let items = songs_list.matchAll(song_search_regex) || [];

	for (const item of items) {
		let lyricMeta = man.createLyric();

		lyricMeta.artist = item[1];
		lyricMeta.title = meta.title;

		let id_song = item[2].match(/\?lyrics=\d+/g);
		request({
			url: 'https://www.eurobeat-prime.com/lyrics.php' + id_song,
			headers: headers,
		}, (err, res, body) => {
			if (err || res.statusCode != 200) {
				return;
			}

			let lyric = body.match(/(?<=Search database<.a>)[\S\s]+?(?=<.div>)/)[0];
			lyric = lyric
				.replace(/&#([0-9]+);/g, function(_, dec) {
					return String.fromCodePoint(dec);
				})
				.replace(/<br.*?>/g, '')
			;

			lyricMeta.lyricText = lyric.trim();
			man.addLyric(lyricMeta);
		});
	}
}