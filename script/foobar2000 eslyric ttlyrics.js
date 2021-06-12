// based on ttplayer 0.0.3.js by ohyeah

function get_my_name() {
	return "TTLyrics|千千歌词";
}

function get_version() {
	return "1";
}

function get_author() {
	return "mdconals bts meal";
}

var SERVER = "http://lyrics.ttlyrics.com:86";

function start_search(info, callback) {
	var http_client = utils.CreateHttpClient();
	var url;

	var artist = info.Artist;
	var title = info.Title;
	var results = [];

	url = SERVER + "/api/search/?title=" + process_keywords(title) + "&artist=" + process_keywords(artist);
	var xml_text = http_client.Request(url);
	if (http_client.StatusCode != 200) {
		dbg_trace("request url[" + url + "] error : " + http_client.StatusCode);
		return;
	}

	var xmlDoc;
	try {
		xmlDoc = new ActiveXObject("Msxml2.DOMDocument");
	} catch (e) {
		dbg_trace("create object 'MSXML.DOMDocument' error : " + e.message);
		return;
	}

	var _new_lyric = callback.CreateLyric();

	xmlDoc.loadXML(xml_text);
	var lyrics = xmlDoc.getElementsByTagName("lrc");
	for (var i = 0; i < lyrics.length; i++) {
		try {
			results.push({
				title: lyrics[i].getAttribute("title"),
				artist: lyrics[i].getAttribute("artist"),
				id: lyrics[i].getAttribute("id")
			});
		} catch (e) {
			dbg_trace(e.message);
			continue;
		}
	}

	for (var i = 0; i < results.length; i++) {
		if (callback.IsAborting()) {
			dbg_trace("user aborted");
			break;
		}
		url = SERVER + "/api/download/?id=" + results[i].id;
		var lyric_text = http_client.Request(url);
		if (http_client.StatusCode != 200) {
			dbg_trace("request url[" + url + "] error : " + http_client.StatusCode);
			continue;
		}
		//add lyric to eslyric
		_new_lyric.Title = results[i].title;
		_new_lyric.Artist = results[i].artist;
		_new_lyric.Source = get_my_name();
		_new_lyric.LyricText = lyric_text;
		_new_lyric.Location = url;
		callback.AddLyric(_new_lyric);
		if (i % 2 == 0) callback.Refresh();
	}

	_new_lyric.Dispose();

}

function dbg_trace(s) {
	fb.trace("TTLyrics: " + s);
}

function process_keywords(str) {
	var s = str;
	s = s.toLowerCase();
	s = s.replace(/\'|·|\$|\&|–/g, "");
	//trim all spaces
	s = s.replace(/(\s*)|(\s*$)/g, "");
	//truncate all symbols
	s = s.replace(/\(.*?\)|\[.*?]|{.*?}|（.*?/g, "");
	s = s.replace(/[-/:-@[-`{-~]+/g, "");
	s = s.replace(/[\u2014\u2018\u201c\u2026\u3001\u3002\u300a\u300b\u300e\u300f\u3010\u3011\u30fb\uff01\uff08\uff09\uff0c\uff1a\uff1b\uff1f\uff5e\uffe5]+/g, "");
	//fb.trace(s);
	return s;
}
