export function getConfig(cfg) {
	cfg.name = 'bilibili 彈幕';
	cfg.version = '2023.07.08';
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

		const rawSeconds = parseFloat(time_s);
		/* 以下 Bing AI */
		const minutes = Math.floor(rawSeconds / 60);
		const seconds = (rawSeconds % 60).toFixed(3);
		const [intSeconds, ms] = seconds.split('.');
		const formattedTime = `${minutes.toString().padStart(2, '0')}.${intSeconds.padStart(2, '0')}.${ms.padEnd(3, '0')}`;
		/* 以上 Bing AI */

		lines += '\n[' + formattedTime + '\]' + text;
	}
	context.lyricText = lines;
}