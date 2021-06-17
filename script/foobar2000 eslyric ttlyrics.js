// modified from ttplayer 0.0.3.js by ohyeah

function get_my_name(sub_a, sub_b) {
	if (sub_a) {
		return "TTLyrics" + ": " + (sub_a) + "|千千歌词" + "：" + (sub_b || sub_a);
	}
	return "TTLyrics|千千歌词";
}

function get_version() {
	return "5";
}

function get_author() {
	return "mdconals bts meal";
}

var SERVER = "http://lyrics.ttlyrics.com:86";
var LRC_MAX = 3;

function start_search(info, callback) {
	var http_client = utils.CreateHttpClient();
	var url;

	var artist = info.Artist;
	var title = info.Title;
	var results = [];

	url = SERVER + "/api/search/?title=" + encodeURIComponent(title) + "&artist=" + encodeURIComponent(artist);
	var xml_text = http_client.Request(url);
	if (http_client.StatusCode != 200) {
		log(http_client.StatusCode + ": " + url);
		return;
	}

	var xmlDoc;
	try {
		xmlDoc = new ActiveXObject("Msxml2.DOMDocument");
	} catch (e) {
		log("create object 'MSXML.DOMDocument' error: " + e.message);
		return;
	}

	var _new_lyric = callback.CreateLyric();

	xmlDoc.loadXML(xml_text);
	var lyrics = xmlDoc.getElementsByTagName("lrc");
	log(lyrics[0].getAttribute("artist") + "／" + (lyrics.length - 1) + "个→" + LRC_MAX + "个");
	for (var i = 1; i < lyrics.length; i++) {
		try {
			results.push({
				//title: lyrics[i].getAttribute("title"),
				//artist: lyrics[i].getAttribute("artist").slice(lyrics[i].getAttribute("artist").indexOf("]") + 1),
				// circumvent ESLyric's arcane match filtering
				title: title,
				artist: artist,
				source: lyrics[i].getAttribute("artist").slice(1, lyrics[i].getAttribute("artist").indexOf("]")),
				id: lyrics[i].getAttribute("id")
			});
		} catch (e) {
			log(e.message);
			continue;
		}
	}

	var lrc_success_n = 0;
	for (var i = 0; lrc_success_n < LRC_MAX; i++) {
		if (callback.IsAborting()) {
			log("user aborted");
			break;
		}
		url = SERVER + "/api/download/?id=" + results[i].id;
		var lyric_text = http_client.Request(url);
		if (http_client.StatusCode != 200) {
			log(http_client.StatusCode + ": " + url);
			continue;
		}
		// add lyric to ESLyric
		if (lyric_text.indexOf("     ") > 0) {
			_new_lyric.Title = results[i].title;
			_new_lyric.Artist = results[i].artist;
			_new_lyric.Source = get_my_name(results[i].source + ": no CHN", results[i].source + "／单语");
			_new_lyric.LyricText = lyric_text.replace(/     .+/g, "");
			_new_lyric.Location = url;
			callback.AddLyric(_new_lyric);

			_new_lyric.Title = results[i].title;
			_new_lyric.Artist = results[i].artist;
			_new_lyric.Source = get_my_name(results[i].source + ": with CHN", results[i].source + "／双语");
			_new_lyric.LyricText = lyric_text;
			_new_lyric.Location = url;
			callback.AddLyric(_new_lyric);
		} else {
			_new_lyric.Title = results[i].title;
			_new_lyric.Artist = results[i].artist;
			_new_lyric.Source = get_my_name(results[i].source);
			_new_lyric.LyricText = lyric_text;
			_new_lyric.Location = url;
			callback.AddLyric(_new_lyric);
		}
		if (i % 2 == 0) callback.Refresh();
		lrc_success_n++;
	}

	_new_lyric.Dispose();
}

function log(s) {
	fb.trace("TTLyrics: " + s);
}
