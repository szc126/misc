// 記得把繁簡轉換關掉喎
// remember to turn off Trad. Chn. to Simp. Chn. conversion
// 繁体字→簡体字変換の無効化もお忘れなく
// Tools > ESLyric > 高級搜索設置
// Tools > ESLyric > Search Settings

export function getConfig(cfg) {
	cfg.name = 'VocaDB';
	cfg.version = '2023.08.23';
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
	// 若是相關文件夾外則取消搜索
	// skip songs that aren't in my vocal synth folder
	// 特定フォルダー外のものを無視
	//
	// ☞ 量體裁衣
	// ☞ modify as needed
	// ☞ 自身の状況に応じて修正をしましょう
	//
	if (meta.path.indexOf('-v\\') == -1) {
		console.log('範圍外，已跳過／Skipped: Out of scope');
		return;
	}

	let headers = {
		'Accept': 'application/json',
		'User-Agent': 'VocaDB for ESLyric for foobar2000',
	};
	const N_LYRICS_MAX = 5;

	for (let i_server = 0; i_server < SERVERS.length; i_server++) {
		// https://vocadb.net/api
		let url = SERVERS[i_server] + '/api/songs?query=' + encodeURIComponent(meta.title);
		// https://github.com/VocaDB/vocadb/blob/main/VocaDbWeb/Controllers/Api/SongApiController.cs
		// nameMatchMode
		// https://github.com/VocaDB/vocadb/blob/main/VocaDbModel/Service/NameMatchMode.cs
		url += '&maxResults=' + N_LYRICS_MAX + '&preferAccurateMatches=true&nameMatchMode=Auto&fields=Lyrics';
		// some magic string from
		// the "Advanced filters" drop down at
		// https://vocadb.net/Search?filter=&searchType=Song
		// for songs that have lyrics registered
		url += '&advancedFilters[0][filterType]=Lyrics&advancedFilters[0][negate]=false&advancedFilters[0][param]=*';
		//console.log(url);

		request({
			url: url,
			headers: headers,
		}, (err, res, body) => {
			if (err || res.statusCode != 200) {
				return;
			}

			body = JSON.parse(body);
			for (let i_item = 0; i_item < body['items'].length; i_item++) {
				let item = body['items'][i_item];
				//console.log(SERVERS[i_server] + '/S/' + item['id']);
				//console.log(item['artistString'] + '／' + item['name']);
				let lyricMeta = man.createLyric();
				lyricMeta.title = item['name'];
				lyricMeta.artist = item['artistString'];
				for (let i_lyric = 0; i_lyric < item['lyrics'].length; i_lyric++) {
					// XXX: new ESLyric cannot write source?
					lyricMeta.source = SERVERS_NAMES[i_server];
					lyricMeta.source += ': ' + item['lyrics'][i_lyric]['translationType'];
					if (item['lyrics'][i_lyric]['cultureCodes'][0] != '') lyricMeta.source += ': ' + item['lyrics'][i_lyric]['cultureCodes'].join(', ');
					// XXX
					lyricMeta.album = '(' + lyricMeta.source + ')';
					lyricMeta.location = SERVERS[i_server] + '/S/' + item['id'];
					lyricMeta.lyricText = item['lyrics'][i_lyric]['value'];
					if (item['lyrics'][i_lyric]['translationType'] == 'Translation') {
						let tlSo = item['lyrics'][i_lyric]['source'];
						let tlUrl = item['lyrics'][i_lyric]['url'];
						// or should translation attribution be written as [by:hogehoge <https://example.com/>]?
						if (tlSo || tlUrl) {
							let tlAttr = 'Translation:\n';
							tlAttr += tlSo && tlSo + '\n' || '';
							tlAttr += tlUrl && tlUrl + '\n' || '';
							lyricMeta.lyricText = tlAttr + '───\n' + lyricMeta.lyricText;
						}
					}
					man.addLyric(lyricMeta);
				}
			}
		});
	}
}