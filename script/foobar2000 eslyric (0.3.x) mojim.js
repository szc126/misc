function get_my_name() {
	return "Mojim|魔鏡";
}

function get_version() {
	return "2";
}

function get_author() {
	return "manipulate mansplain malewife";
}

var wtf = true; // eslyric : calls HttpSendRequest error : [12157]

function start_search(info, callback) {
	var _new_lyric = callback.CreateLyric();

	var artist = info.Artist;
	var album = info.Album;
	var title = info.Title;
	var url;

	var http_client = utils.CreateHttpClient();
	http_client.addHttpHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0");

	url = "https://mojim.com/" + encodeURIComponent(title.replace(/[+-]/g, ' ')) + ".html?g3";
	if (wtf) url = "http://api.allorigins.win/get?url=" + encodeURIComponent(url);
	log(url);
	var response = http_client.Request(url);
	if (http_client.StatusCode != 200) {
		log("[ERROR]" + http_client.StatusCode);
		return;
	}
	if (wtf) response = JSON.parse(response)["contents"];

	var items = response.match(/<dd [\S\s]+?<.dd>/g);

	for (var i_item = 1; i_item < items.length; i_item++) {
		var lrc_meta_raw = items[i_item].match(/.+mxsh_ss.+/g);

		var lrc_meta = {
			artist: lrc_meta_raw[1].match(/<a .+>(.+)<.a>/)[1],
			album: lrc_meta_raw[2].match(/<a .+>(.+)<.a>/)[1],
			title: lrc_meta_raw[3].replace(/<font [^<>]+>|<.font>/g, "").match(/<a .+>(.+)<.a>/)[1].replace(/^[0-9]+\./, ''),
			url: lrc_meta_raw[3].match(/<a href="([^"]+)"/)[1]
		}
		log(lrc_meta.artist + "／" + lrc_meta.album + "／" + lrc_meta.title);

		// discard partial title match
		// to avoid downloading 200 irrelevant webpages
		// note that parentheses etc are ignored in search results
		//if (!lrc_meta_raw[3].match(/[0-9].\<font.+<.font><.a>/)) {
		if (lrc_meta.title.replace(/[\s()+-]/g, '').toLowerCase() != title.replace(/[\s()+-]/g, '').toLowerCase()) {
			log("Skipped");
			continue;
		}

		if (callback.IsAborting()) {
			log("User aborted");
			break;
		}

		url = "https://mojim.com" + lrc_meta.url;
		if (wtf) url = "http://api.allorigins.win/get?url=" + encodeURIComponent(url);
		log(url);
		var response = http_client.Request(url);
		if (http_client.StatusCode != 200) {
			log("[ERROR]" + http_client.StatusCode);
			return;
		}
		if (wtf) response = JSON.parse(response)["contents"];

		var lyric = response.match(/<dl id=.fsZx1. [\S\s]+?<.dl>/)[0];
		lyric = lyric
			.replace(/&#([0-9]+)/g, function(_, dec) {
				return String.fromCharCode(dec);
			})
			.replace(/<br[^>]*>/g, "\n")
			.replace(/.+Mojim.+\n/g, "")
			.replace(/^[\S\s]+<.dt>\n+[^\n]+\n+/, "") // /[^\n]+\n+/ is song title + \n\n
			.replace(/\n+<ol>[\S\s]+/, "")
		;

		_new_lyric.Title = lrc_meta.title;
		_new_lyric.Album = lrc_meta.album;
		_new_lyric.Artist = lrc_meta.artist;
		_new_lyric.Source = get_my_name();
		_new_lyric.LyricText = lyric;
		callback.AddLyric(_new_lyric);

		if (i_item % 2 == 0) callback.Refresh(); // 這啥？
	}

	_new_lyric.Dispose();
}

function log(s) {
	fb.trace("Mojim: " + s);
}
