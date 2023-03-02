// modified from ttplayer 0.0.3.js by ohyeah

function get_my_name(sub_a, sub_b) {
	if (sub_a) {
		return "TTLyrics" + ": " + (sub_a) + "|千千歌词" + "：" + (sub_b || sub_a);
	}
	return "TTLyrics|千千歌词";
}

function get_version() {
	return "7";
}

function get_author() {
	return "mdconals bts meal";
}

var SERVER = "http://lyrics.ttlyrics.com:86";
var SKIP = "咪咕 新千千";
var HTML_ENTITY_UN = {
	"amp": "&",
	"apos": "\'",
}

function start_search(info, callback) {
	var http_client = utils.CreateHttpClient();
	var xmlDoc;
	try {
		xmlDoc = new ActiveXObject("Msxml2.DOMDocument");
	} catch (e) {
		log("[ERROR]" + "Msxml2.DOMDocument: " + e.message);
		return;
	}
	var _new_lyric = callback.CreateLyric();

	var artist = info.Artist;
	var title = info.Title;
	var url;

	url = SERVER + "/api/search/?title=" + encodeURIComponent(title) + "&artist=" + encodeURIComponent(artist);
	log(url);
	var xml_search = http_client.Request(url);
	xmlDoc.loadXML(xml_search);
	if (http_client.StatusCode != 200) {
		var errmsg = xmlDoc.getElementsByTagName("result")[0].getAttribute("errmsg");
		log("[ERROR]" + http_client.StatusCode + " " + errmsg);
		return;
	}

	var tags_lrc = xmlDoc.getElementsByTagName("lrc");
	log(tags_lrc[0].getAttribute("artist") + "／" + (tags_lrc.length - 1) + "个");
	for (var i = 1; i < tags_lrc.length; i++) {
		var lrc_meta = {
			title: tags_lrc[i].getAttribute("title"),
			artist: tags_lrc[i].getAttribute("artist").slice(tags_lrc[i].getAttribute("artist").indexOf("]") + 1),
			album: tags_lrc[i].getAttribute("album"),
			source: tags_lrc[i].getAttribute("artist").slice(1, tags_lrc[i].getAttribute("artist").indexOf("]")),
			id: tags_lrc[i].getAttribute("id")
		}
		log(lrc_meta.source + "／" + lrc_meta.artist + "／" + lrc_meta.title);

		if (SKIP.indexOf(lrc_meta.source) > -1) {
			log("    " + "Skipped");
			continue;
		}

		if (callback.IsAborting()) {
			log("User aborted");
			break;
		}

		url = SERVER + "/api/download/?id=" + lrc_meta.id;
		log("    " + url);
		var lrc = http_client.Request(url);
		if (http_client.StatusCode != 200) {
			xmlDoc.loadXML(lrc);
			var errmsg = xmlDoc.getElementsByTagName("result")[0].getAttribute("errmsg");
			log("    [ERROR]" + http_client.StatusCode + " " + errmsg);
			continue;
		}

		lrc = lrc.replace(/&(\w+);/g, function(_, k) {
			return HTML_ENTITY_UN[k];
		});

		if (
			lrc.indexOf("暂无歌词") > 0 ||
			lrc.indexOf("纯音乐") > 0
		) {
			// no-op
		} else if (lrc.indexOf("     ") > 0) {
			_new_lyric.Title = lrc_meta.title;
			_new_lyric.Artist = lrc_meta.artist;
			_new_lyric.Source = get_my_name(lrc_meta.source + ": no CHN", lrc_meta.source + "／单语");
			_new_lyric.LyricText = lrc.replace(/     .+/g, "");
			_new_lyric.Location = url;
			callback.AddLyric(_new_lyric);

			_new_lyric.Title = lrc_meta.title;
			_new_lyric.Artist = lrc_meta.artist;
			_new_lyric.Source = get_my_name(lrc_meta.source + ": with CHN", lrc_meta.source + "／双语");
			_new_lyric.LyricText = lrc;
			_new_lyric.Location = url;
			callback.AddLyric(_new_lyric);
		} else {
			_new_lyric.Title = lrc_meta.title;
			_new_lyric.Artist = lrc_meta.artist;
			_new_lyric.Source = get_my_name(lrc_meta.source);
			_new_lyric.LyricText = lrc;
			_new_lyric.Location = url;
			callback.AddLyric(_new_lyric);
		}
		if (i % 2 == 0) callback.Refresh();
	}

	_new_lyric.Dispose();
}

function log(s) {
	fb.trace("TTLyrics: " + s);
}
