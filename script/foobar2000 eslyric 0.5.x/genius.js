export function getConfig(cfg) {
	cfg.name = 'Genius';
	cfg.version = '2023.04.04';
	cfg.author = 'transgender walmart';
	cfg.useRawMeta = false;
}

export function getLyrics(meta, man) {
	let headers = {
		'User-Agent': 'Genius for ESLyric for foobar2000',
	};
	let url = 'https://genius.com/api/search?per_page=2&q=' + encodeURIComponent(meta.title + ' ' + meta.artist);

	request({
		url: url,
		headers: headers,
	}, (err, res, body) => {
		if (err || res.statusCode != 200) {
			return;
		}

		body = body.replace(/\u200b/g, '');

		body = JSON.parse(body);
		for (let i_hit = 0; i_hit < body['response']['hits'].length; i_hit++) {
			let lyricMeta = man.createLyric();
			lyricMeta.title = body['response']['hits'][i_hit]['result']['title_with_featured'];
			lyricMeta.artist = body['response']['hits'][i_hit]['result']['primary_artist']['name'];

			request({
				url: 'https://genius.com/songs/' + body['response']['hits'][i_hit]['result']['id'] + '/embed.js',
				headers: headers,
			}, (err, res, body) => {
				if (err || res.statusCode != 200) {
					return;
				}

				body = body.replace(/\u200b/g, '');

				let lyric = body.match(/(?<=<p>).+(?=<..p>)/);
				/*
				lyric = lyric && lyric[0].replace(/\\+/g, function(escs) {return escs.substring(0, escs.length - 1)});
				lyric = JSON.parse('"' + lyric + '"');
				*/
				lyric = lyric && lyric[0]
					.replace(/\\n/g, '\n')
					.replace(/\\|<.+?>/g, '')
				;

				lyricMeta.lyricText = lyric;
				man.addLyric(lyricMeta);
			});
		}
	});
}