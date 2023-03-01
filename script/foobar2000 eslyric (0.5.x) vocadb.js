// 記得把繁簡轉換關掉喎
// remember to turn off Trad. Chn. to Simp. Chn. conversion
// 繁体字→簡体字変換の無効化もお忘れなく
// Tools > ESLyric > 高級搜索設置
// Tools > ESLyric > Search Settings

export function getConfig(cfg) {
	cfg.name = 'VocaDB';
	cfg.version = '2023.03.01';
	cfg.author = 'transgender queen boudica';
	cfg.useRawMeta = false;
}

let SERVERS = [
	'https://vocadb.net',
	'https://utaitedb.net',
];

let SERVERS_NAMES = [
	'VocaDB',
	'UtaiteDB',
];

export function getLyrics(meta, man) {
	// 相關文件夾外則取消搜索
	// skip songs that aren't in my vocal synth folder
	// 特定フォルダー外のものを無視
	//
	// ☞ 量體裁衣
	// ☞ modify as needed
	// ☞ 自身の状況に応じて修正をしましょう
	//
	if (meta.path.indexOf('ボカロUTAU') == -1) {
		console.log('範圍外，已跳過／Skipped: Out of scope');
		return;
	}

	for (var i_server = 0; i_server < SERVERS.length; i_server++) {
		let headers = {
			'Accept': 'application/json',
			'User-Agent': 'VocaDB for ESLyric for foobar2000',
		};
		let url = SERVERS[i_server] + '/api/songs?query=' + encodeURIComponent(meta.title);
		url += '&maxResults=5&preferAccurateMatches=true&nameMatchMode=Exact&fields=Lyrics';
		url += '&advancedFilters[0][description]=Lyrics%3A+Any+language&advancedFilters[0][filterType]=Lyrics&advancedFilters[0][negate]=false&advancedFilters[0][param]=*';
		//console.log(url);

		request({
			url: url,
			headers: headers,
		}, (err, res, body) => {
			if (err || res.statusCode != 200) {
				return;
			}

			body = JSON.parse(body);
			for (var i_item = 0; i_item < body['items'].length; i_item++) {
				var item = body['items'][i_item];
				//console.log(SERVERS[i_server] + '/S/' + item['id']);
				//console.log(item['artistString'] + '／' + item['name']);
				for (var i_lyric = 0; i_lyric < item['lyrics'].length; i_lyric++) {
					let lyricMeta = man.createLyric();
					lyricMeta.title = item['name'];
					lyricMeta.artist = item['artistString'];
					// XXX: new ESLyric cannot write source?
					lyricMeta.source = SERVERS_NAMES[i_server];
					lyricMeta.source += ': ' + item['lyrics'][i_lyric]['translationType']
					if (item['lyrics'][i_lyric]['cultureCode'] != '') lyricMeta.source += ': ' + item['lyrics'][i_lyric]['cultureCode'];
					// XXX
					lyricMeta.album = '(' + lyricMeta.source + ')';
					lyricMeta.lyricText = item['lyrics'][i_lyric]['value'];
					man.addLyric(lyricMeta);
				}
			}
		});
	}
}