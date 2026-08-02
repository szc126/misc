export function getConfig(cfg) {
	cfg.name = '벅스 Bugs!';
	cfg.version = '2023.06.12';
	cfg.author = 'rabbits in drag';

	cfg.useRawMeta = false;

	cfg.parsePlainText = true;
	cfg.fileType = 'bugs';
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

		let ids = body.match(/(?<=listen\(').+(?='\))/g) || [];
		let titles = body.match(/(?<=^title.+>).+(?=<.a>)/gm) || [];
		let artists = body.match(/(?<=artist'.;\r\n">).+(?=<.a>)/g) || [];
		let albums = body.match(/(?<=album'.;\r\n">).+(?=<.a>)/g) || [];

		for (let i_id = 0; i_id < Math.min(ids.length, N_LYRICS_MAX); i_id++) {
			// https://github.com/limerainne/mp3tag-ws-bugs/blob/master/Bugs%232.%20곡%20ID%20-%20동기가사.src
			request({
				url: 'https://music.bugs.co.kr/player/lyrics/T/' + ids[i_id],
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				let lyricMeta = man.createLyric();
				lyricMeta.title = titles[i_id];
				lyricMeta.artist = artists[i_id];
				lyricMeta.album = albums[i_id];

				body = JSON.parse(body);
				if (body['lyrics'] == '') {
					request({
						url: 'https://music.bugs.co.kr/player/lyrics/N/' + ids[i_id],
						headers: headers,
					}, (err, res, body) => {
						if (err || res.statusCode != 200) {
							return;
						}

						body = JSON.parse(body);
						if (body['lyrics'] == '') {
							return;
						}
						lyricMeta.lyricText = body['lyrics'];
					});
				} else {
					lyricMeta.fileType = 'bugs';
					lyricMeta.lyricText = body['lyrics'];
				}

				man.addLyric(lyricMeta);
			});
		}
	});
}

export function parseLyric(context) {
	let hold = context.lyricText.split(/[|＃]/g);
	let lines = '';
	for (let i = 0; i < hold.length; i += 2) {
		lines += '[00:' + hold[i] + ']' + hold[i+1] + '\n';
	}
	context.lyricText = lines;
}