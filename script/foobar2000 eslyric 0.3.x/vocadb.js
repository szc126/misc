function get_my_name() {
	return "VocaDB";
}

function get_version() {
	return "2";
}

function get_author() {
	return "mccune-reischauer romanization";
}

var SERVERS = [
	"http://vocadb.net",
	"http://utaitedb.net"
];

var SERVERS_NAMES = [
	"VocaDB",
	"UtaiteDB"
];

var wtf = true; // eslyric : calls HttpSendRequest error : [12157]

function start_search(info, callback) {
	var _new_lyric = callback.CreateLyric();

	var artist = info.Artist;
	var title = info.Title;
	var rawPath = info.RawPath;
	var url;

	// skip songs that aren't in my vocal synth folder
	if (rawPath.indexOf("ボカロUTAU") == -1) {
		log("Out of scope; skipping...");
		return;
	}

	var http_client = utils.CreateHttpClient();
	http_client.addHttpHeader("Accept", "application/json");
	http_client.addHttpHeader("User-Agent", "VocaDB for ESLyric for foobar2000");

	for (var i_server = 0; i_server < SERVERS.length; i_server++) {
		url = SERVERS[i_server] + "/api/songs?query=" + encodeURIComponent(title);
		url += "&songTypes=Original,Mashup&maxResults=3&preferAccurateMatches=true&nameMatchMode=Exact&fields=Lyrics";
		if (wtf) url = "http://api.allorigins.win/get?url=" + encodeURIComponent(url);
		log(url);
		var response = http_client.Request(url);
		if (http_client.StatusCode != 200) {
			log("[ERROR]" + http_client.StatusCode);
			return;
		}
		response = JSON.parse(response);
		if (wtf) response = JSON.parse(response["contents"]);

		for (var i_item = 0; i_item < response["items"].length; i_item++) {
			var item = response["items"][i_item];

			if (callback.IsAborting()) {
				log("User aborted");
				break;
			}

			log(SERVERS[i_server] + "/S/" + item["id"]);
			log(item["artistString"] + "／" + item["name"]);

			for (var i_lyric = 0; i_lyric < item["lyrics"].length; i_lyric++) {
				_new_lyric.Title = item["name"];
				_new_lyric.Artist = item["artistString"];
				_new_lyric.Source = SERVERS_NAMES[i_server];
				_new_lyric.Source += ": " + item["lyrics"][i_lyric]["translationType"]
				if (item["lyrics"][i_lyric]["cultureCode"] != "") _new_lyric.Source += ": " + item["lyrics"][i_lyric]["cultureCode"];
				_new_lyric.LyricText = item["lyrics"][i_lyric]["value"];
				callback.AddLyric(_new_lyric);
			}

			if (i_item % 2 == 0) callback.Refresh(); // 這啥？
		}
	}

	_new_lyric.Dispose();
}

function log(s) {
	fb.trace("VocaDB: " + s);
}
