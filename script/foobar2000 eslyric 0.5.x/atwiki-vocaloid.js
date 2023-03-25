// 記得把繁簡轉換關掉喎
// remember to turn off Trad. Chn. to Simp. Chn. conversion
// 繁体字→簡体字変換の無効化もお忘れなく
// Tools > ESLyric > 高級搜索設置
// Tools > ESLyric > Search Settings

export function getConfig(cfg) {
	cfg.name = 'atwiki (ボカロ系)';
	cfg.version = '2023.03.22';
	cfg.author = 'transgender judith beheading holofernes';
	cfg.useRawMeta = false;
}

let SERVERS = [
	'https://w.atwiki.jp/hmiku/',
	'https://w.atwiki.jp/utauuuta/',
];

let SERVERS_NAMES = [
	'初音ミク Wiki',
	'UTAU楽曲データベース',
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

	let headers = {
		// 下手だけど一旦慎重に
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
	};
	for (let i_server = 0; i_server < SERVERS.length; i_server++) {
		let url = SERVERS[i_server] + '?page=' + encodeURIComponent(meta.title);
		//console.log(url);

		request({
			url: url,
			headers: headers,
		}, (err, res, body) => {
			if (res.statusCode == 404) {
				// →検索してみる
			} else if (err || res.statusCode != 200) {
				return;
			}

			if (res.statusCode == 404) {
				console.log(SERVERS[i_server] + '｜Wiki內搜索中／No such page. Searching');
				url = SERVERS[i_server] + 'search?keyword=' + encodeURIComponent(
					// 「曲紹介」というキーワードを利用してアルバムなどを排除
					meta.title + ' ' + meta.artist.replace(/feat\./g, '') + ' 曲紹介'
				);
				url += '&search_field=source&cmp=cmp';

				request({
					url: url,
					headers: headers,
				}, (err, res, body) => {
					if (err || res.statusCode != 200) {
						return;
					}

					let song_ids = body.match(/(?<=pageid=)\d+/g) || [];
					for (let i_song_id = 0; i_song_id < song_ids.length; i_song_id++) {
						request({
							url: SERVERS[i_server] + 'pages/' + song_ids[i_song_id] + '.html',
							headers: headers,
						}, (err, res, body) => {
							if (err || res.statusCode != 200) {
								return;
							}

							readPage(i_server, body);
						});
					}
				});

				return;
			} else if (body.indexOf('曖昧さ回避のためのページ') > 1) {
				console.log(SERVERS[i_server] + '｜曖昧さ回避／Disambiguation');
				let song_urls = body.match(/(?<=<li>.+の曲.+<a href=")[^"]+(?=" [^<>]+>.+<.a>)/g);
				for (let i_song_url = 0; i_song_url < song_urls.length; i_song_url++) {
					request({
						url: 'https:' + song_urls[i_song_url],
						headers: headers,
					}, (err, res, body) => {
						if (err || res.statusCode != 200) {
							return;
						}

						readPage(i_server, body);
					});
				}

				return;
			} else if (body.indexOf('曲紹介') == -1) {
				console.log(SERVERS[i_server] + '｜不是歌曲項目／Not a song page');
				// あったら曖昧さ回避になるため検索しても出てこないはず

				return;
			}

			readPage(i_server, body);
		});
	}

	function readPage(i_server, body) {
		// in terms of memory usage, this is probably stupid
		let title = body;
		let composer = body;
		let vocalist = body;
		let lyric = body;

		title = title.match(/(?<=曲名[：:]『).+(?=』)/g) || title.match(/(?<=<h2>).+(?=<.h2>)/g);
		title = title && title[0]
			.replace(/<u>(.+)<.u>/g, '$1')
			.replace(/ &gt; <a .+/g, '') // 曖昧さ回避の場合 hmiku
			.replace(/／[^<>]+?/g, '') // 曖昧さ回避の場合 utauuuta
			.replace(/<a [^<>]+>(.+?)<.a>/g, '$1')
			.replace(/<span [^<>]+>(.+?)<.span>/g, '$1') // utauuta class="pagename"
		;
		composer = composer.match(/(?<=\n作曲[：:]).+/g);
		composer = composer && composer[0]
			.replace(/<a [^<>]+>(.+?)<.a>/g, '$1')
		;
		vocalist = vocalist.match(/(?<=\n唄[：:]|\n唄（.+?）[：:]).+/g);
		vocalist = vocalist && vocalist[0]
			.replace(/<a [^<>]+>(.+?)<.a>/g, '$1')
		;
		lyric = lyric.match(/(?<=<h3 [^<>]+>歌詞<.h3>).+?(?=<h3 )/gs);
		lyric = lyric && lyric[0]
			.replace(/\n/g, '')
			.replace(/<div>|<br .>/g, '\n')
			.replace(/<[a-z]+ [^<>]+>|<\/?[a-z]+>/g, '')
			.trim()
		;

		let lyricMeta = man.createLyric();
		lyricMeta.title = title;
		lyricMeta.artist = composer + ' feat. ' + vocalist;
		// XXX: new ESLyric cannot write source?
		lyricMeta.source = SERVERS_NAMES[i_server];
		// XXX
		lyricMeta.album = '(' + lyricMeta.source + ')';
		lyricMeta.lyricText = lyric;
		man.addLyric(lyricMeta);
	}
}

/*
notes
- https://w.atwiki.jp/hmiku/?page=乙女解剖
	- 唄（原曲）：初音ミク
	- 曲名：『乙女解剖』(おとめかいぼう)
- https://w.atwiki.jp/hmiku/?page=パンダヒーロー
	- DIVA：GUMI
- https://w.atwiki.jp/hmiku/?page=ぽっぴっぽー
	- TODO: ver.
- https://w.atwiki.jp/hmiku/?page=モザイクロール
	- TODO: ver.
- https://w.atwiki.jp/hmiku/?page=月西江
	- TODO: translation etc.
- https://w.atwiki.jp/hmiku/?page=ECHO%2FCRUSHER-P
	- TODO: translation etc.
- https://w.atwiki.jp/hmiku/?page=Do+You+%26+So+You
	- TODO: unescape HTML entities
- https://w.atwiki.jp/hmiku/?page=ごめんね%20ごめんね
	- TODO: #region
*/
