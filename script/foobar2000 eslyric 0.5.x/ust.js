// しょうもなさそうすぎてやるしかなかった

export function getConfig(cfg) {
	cfg.name = 'UST Parser';
	cfg.version = '2023.03.02';
	cfg.author = 'asexual larry nothing forever';
	cfg.parsePlainText = true;
	cfg.fileType = 'ust';
}

export function parseLyric(context) {
	let tempo = context.lyricText.match(/(?<=Tempo=)[\d.]+(?=[\r\n]+)/g);
	//if (tempo.length > 0) return; // TODO
	tempo = tempo && Number(tempo[0]);
	let notes = [];
	let lines = '[00:00.00]';
	let secSongElapsed = 0;
	for (const match of context.lyricText.matchAll(/Length=([\d]+)[\r\n]+Lyric=(.+)[\r\n]+/g)) {
		const length = Number(match[1]);
		let lyric = match[2];
		lyric = (lyric == 'R' || lyric == 'r') && '　' || lyric;
		notes.push(length, lyric);
	}
	for (let i_note = 0; i_note < notes.length; i_note += 2) {
		const length = notes[i_note + 0];
		const lyric = notes[i_note + 1];
		const secLength = lengthToSecond(tempo, length);

		if (lyric == '　' && length >= 120) {
			secSongElapsed += secLength;
			lines += '\n[' + formatTime(secSongElapsed * 1000) + ']';
		} else {
			lines += lyric;
			secSongElapsed += secLength;
			lines += '<' + formatTime(secSongElapsed * 1000) + '>';
		}
	}
	lines += '\n[' + formatTime(secSongElapsed * 1000) + ']';

	context.lyricText = lines;
}

function lengthToSecond(tempo, length) {
	return length / tempo / 8;
}

function zpad(n) {
	var s = n.toString();
	return (s.length < 2) ? '0' + s : s;
}

function formatTime(time) {
	var t = Math.abs(time / 1000);
	var h = Math.floor(t / 3600);
	t -= h * 3600;
	var m = Math.floor(t / 60);
	t -= m * 60;
	var s = Math.floor(t);
	var ms = t - s;
	var str = (h ? zpad(h) + ':' : '') + zpad(m) + ':' + zpad(s) + '.' + zpad(Math.floor(ms * 100));
	return str;
}