// 記得把繁簡轉換關掉喎
// Remember to turn off Trad. to Simp. conversion
// Tools > ESLyric > 歌詞選項 > 高級搜索設置

export function getConfig(cfg) {
	cfg.name = 'VocaDB';
	cfg.version = '2023.02.27';
	cfg.author = 'hoshou wa ato nannen?';
	cfg.useRawMeta = false;
}

let SERVERS = [
	'http://vocadb.net',
	'http://utaitedb.net'
];

let SERVERS_NAMES = [
	'VocaDB',
	'UtaiteDB'
];

let wtf = true; // XXX: HttpSendRequestA error - [0x0000013D]

export function getLyrics(meta, man) {
	// skip songs that aren't in my vocal synth folder
	if (meta.path.indexOf('ボカロUTAU') == -1) {
		log('範圍外，已跳過');
		return;
	}

	for (var i_server = 0; i_server < SERVERS.length; i_server++) {
		let headers = {
			'Accept': 'application/json',
			'User-Agent': 'VocaDB for ESLyric for foobar2000',
		}
		let url = SERVERS[i_server] + '/api/songs?query=' + encodeURIComponent(meta.title);
		url += '&songTypes=Original,Mashup&maxResults=3&preferAccurateMatches=true&nameMatchMode=Exact&fields=Lyrics';
		if (wtf) url = 'http://api.allorigins.win/get?url=' + encodeURIComponent(url);
		//console.log(url);

		request({
			url: url,
			headers: headers,
		}, (err, res, body) => {
			if (!err && res.statusCode == 200) {
				let response = JSON.parse(body);
				if (wtf) response = JSON.parse(response['contents']);
				for (var i_item = 0; i_item < response['items'].length; i_item++) {
					var item = response['items'][i_item];

					console.log(SERVERS[i_server] + '/S/' + item['id']);
					console.log(item['artistString'] + '／' + item['name']);

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
			}
		});
	}
}