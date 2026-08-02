export function getConfig(cfg) {
	cfg.name = 'bilibili 彈幕';
	cfg.version = '2026.06.12';
	cfg.author = 'live laugh love';
	cfg.parsePlainText = true;
	cfg.fileType = 'xml';
}

export function parseLyric(context) {
	let lines = '';
	let root = mxml.loadString(context.lyricText);

	for (
		let node = root.findElement('d');
		node != null;
		node = node.getNextSibling()
	) {
		let p = node.getAttr('p');
		let time_s = p.split(',')[0];
		let text = node.getText();

		lines += '\n[00:' + time_s + '\]' + text;
	}
	context.lyricText = lines;
}