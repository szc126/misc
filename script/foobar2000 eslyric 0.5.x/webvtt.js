export function getConfig(cfg) {
	cfg.name = 'WebVTT Parser';
	cfg.version = '2023.04.05';
	cfg.author = '10 games collection (cd)';
	cfg.parsePlainText = true;
	cfg.fileType = 'vtt';
}

/*
export function parseLyric(context) {
	let lines = '';
	let last_text = null;
	// XXX: 暫時不理60分鐘後了
	for (const match of context.lyricText.matchAll(/^([0-9:]{3})([0-9:.]{8})[0-9] --> ([0-9:]{3})([0-9:.]{8})[0-9]\n(.+(?:\n.+)*)/gm)) {
		if (match[5].startsWith(last_text)) {
			lines += match[5].slice(last_text.length) + '<' + match[4] + '>';
		} else {
			lines += '\n' + '[' + match[2] + ']' + '<' + match[2] + '>' + match[5].replace(/\n/g, '\n' + '[' + match[2] + ']') + '<' + match[4] + '>';
		}
		last_text = match[5];
	}
	context.lyricText = lines;
}
*/

export function parseLyric(context) {
	context.lyricText = context.lyricText
		// 截斷ms、移除style
		.replace(/^([0-9:.]+)[0-9] --> ([0-9:.]+)[0-9](?: [^\n]+)?/gm, '$1 --> $2')
		// XXX: 暫時不理60分鐘後了
		.replace(/(\d\d):(\d\d)(:\d\d\.\d\d)/gm, function(_, H, M, S) { return M + S; })
		// 移除style
		.replace(/<.+?>/g, '')
	;

	let lines = '';
	for (const match of context.lyricText.matchAll(/^(.+?) --> (.+?)\n(.+)((?:\n.+)*)/gm)) {
		lines += '\n' + '[' + match[1] + ']' + '<' + match[1] + '>' + match[3] + '<' + match[2] + '>' + (match[4] && match[4].replace(/\n/g, '\n' + '[' + match[1] + ']'));
	}
	context.lyricText = lines;
}

/*
notes
- https://github.com/w3c/webvtt.js
- https://www.youtube.com/watch?v=iM8d0SzJTIU DECO*27 - 二息歩行 (Reloaded) feat. 初音ミク
	- can do startsWith
- https://www.youtube.com/watch?v=nPF7lit7Z00 Kikuo - 君はできない子
	- should NOT do startsWith
- https://www.youtube.com/watch?v=35iPH7jJLH0 花が落ちたので、／一二三 feat.初音ミク
	- 雙語（？）跨行
- https://www.youtube.com/watch?v=uFRPeiAEO0M DECO*27 - アンドロイドガール feat. 初音ミク
	- style
- https://www.youtube.com/watch?v=VWVtIg5cdDU 初音ミクの消失(THE END OF HATSUNE MIKU) - cosMo＠暴走P
	- can do startsWith
	- 跨行
*/