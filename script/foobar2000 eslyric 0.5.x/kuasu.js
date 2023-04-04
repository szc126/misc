// 記得把繁簡轉換關掉喔
// remember to turn off Trad. Chn. to Simp. Chn. conversion
// Tools > ESLyric > 進階搜尋設定
// Tools > ESLyric > Search Settings

export function getConfig(cfg) {
	cfg.name = '歌詞正字';
	cfg.version = '2023.04.04';
	cfg.author = 'transgender koxinga';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	// 相關文件夾外則取消搜索
	// skip songs that aren't in my 台語 folder
	// 特定フォルダー外のものを無視
	//
	// ☞ 量體裁衣
	// ☞ modify as needed
	// ☞ 自身の状況に応じて修正をしましょう
	//
	if (meta.path.indexOf('閩') == -1) {
		console.log('範圍外，已跳過／Skipped: Out of scope');
		return;
	}

	let headers = {
		'User-Agent': '歌詞正字 for ESLyric for foobar2000',
	};
	let url = 'https://kuasu.tgb.org.tw/search/?type=song-title&keyword=' + encodeURIComponent(meta.title);

	request({
		url: url,
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		let song_ids = body.match(/(\/song\/\d+\/)/g) || [];
		for (let i_song_id = 0; i_song_id < song_ids.length; i_song_id++) {
			request({
				url: 'https://kuasu.tgb.org.tw' + song_ids[i_song_id],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				let title = body.match(/(?<=original-title.+)[^<>]+/);
				let performer = body.match(/(?<=performer.+演唱人：)[^<>]+/);

				let lyrics_lines_raw = body.match(/<li>[\s\S]+?<.li>/g) || [];
				let lyrics_gb = [];
				let lyrics_tshh = [];
				let lyrics_tshl = [];
				for (let i_lyrics_line_raw = 0; i_lyrics_line_raw < lyrics_lines_raw.length; i_lyrics_line_raw++) {
					let ps = lyrics_lines_raw[i_lyrics_line_raw].match(/(?<=<p class=".+">)[^<>]+(?=\s*<.p>)/g);
					if (!ps) {
						// https://kuasu.tgb.org.tw/song/73/
						// `<li><a href="http://twblg.dict.edu.tw/` [...]
						break;
					}
					lyrics_gb.push(ps[0].replace(/^[｜│]/, ''));
					lyrics_tshh.push(ps[1].replace(/^[.-]$/, ''));
					lyrics_tshl.push(ps[2].replace(/^[.-]$/, ''));
				}

				let lyricMeta = man.createLyric();
				lyricMeta.title = title;
				lyricMeta.artist = performer;

				lyricMeta.source = '歌詞正字: 原文';
				// XXX
				lyricMeta.album = '(' + lyricMeta.source + ')';
				lyricMeta.lyricText = lyrics_gb.join('\n');
				man.addLyric(lyricMeta);

				lyricMeta.source = '歌詞正字: 全漢';
				// XXX
				lyricMeta.album = '(' + lyricMeta.source + ')';
				lyricMeta.lyricText = lyrics_tshh.join('\n');
				man.addLyric(lyricMeta);

				lyricMeta.source = '歌詞正字: 全羅';
				// XXX
				lyricMeta.album = '(' + lyricMeta.source + ')';
				lyricMeta.lyricText = lyrics_tshl.join('\n');
				man.addLyric(lyricMeta);

				lyricMeta.source = '歌詞正字: 原文＋全羅';
				// XXX
				lyricMeta.album = '(' + lyricMeta.source + ')';
				lyricMeta.lyricText = lyrics_gb.flatMap((lyric, i) => [lyric, lyrics_tshl[i]]).join('\n');
				man.addLyric(lyricMeta);

				lyricMeta.source = '歌詞正字: 全漢＋全羅';
				// XXX
				lyricMeta.album = '(' + lyricMeta.source + ')';
				lyricMeta.lyricText = lyrics_tshh.flatMap((lyric, i) => [lyric, lyrics_tshl[i]]).join('\n');
				man.addLyric(lyricMeta);

				lyricMeta.source = '歌詞正字: 原文＋全漢＋全羅';
				// XXX
				lyricMeta.album = '(' + lyricMeta.source + ')';
				lyricMeta.lyricText = lyrics_gb.flatMap((lyric, i) => [lyric, lyrics_tshh[i], lyrics_tshl[i]]).join('\n');
				man.addLyric(lyricMeta);
			});
		}
	});
}