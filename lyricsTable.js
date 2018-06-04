"use strict";

window.onload = function() {
	prepare();
	go(); // initialize stuff
}

let tableHeadSyntax = {
	vw: [ '{| style="width:100%"', '! align=left |' ],
	vlw: [ '{| style="width:100%"', '|' ],
	ulw: [ '{| class="lyrics"', '! ' ],
}

let br = {
	vw: '<br>',
	vlw: '<br />',
	ulw: '<br />',
}

let langIso = {
	zhs: 'zh-cn',
	zht: 'zh-tw',
	yuet: 'zh-hk',
	yues: 'zh-cn',
	
	x: 'en',
}

let headText = {
	vw: {
		en: [ "''Official English'' (公式英訳)" ],
		
		ja: [ "''Japanese'' (日本語歌詞)", "''Romaji'' (ローマ字)" ],
		zht: [ "''Chinese'' (中文歌詞)", "''Pinyin'' (拼音)" ],
		zhs: [ "''Chinese'' (中文歌词)", "''Pinyin'' (拼音)" ],
		ko: [ "''Korean'' (한국어 가사)", "''Romaja'' (로마자)" ],
		yuet: [ "''Cantonese'' (廣東話歌詞)", "''Jyutping'' (粵拼)" ],
		yues: [ "''Cantonese'' (广东话歌词)", "''Jyutping'' (粤拼)" ],
		x: [ "''??'' (??)", "''??'' (??)" ],

		enx: [ '<span class="error">The Vocaloid Wiki does not add unofficial English translations.</span>' ],
		yue: [
			'<span class="error">Traditional (<code>yuet</code>) or simplified (<code>yues</code>)?</span>',
			'<span class="error">Traditional (<code>yuet</code>) or simplified (<code>yues</code>)?</span>'
		],
		zh: [
			'<span class="error">Traditional (<code>zht</code>) or simplified (<code>zhs</code>)?</span>',
			'<span class="error">Traditional (<code>zht</code>) or simplified (<code>zhs</code>)?</span>'
		],
	},
	vlw: {
		en: [ "'''''English'''''" ],
		enx: [ "'''''English'''''" ],
		
		ja: [ "'''''Japanese'''''", "'''''Romaji'''''" ],
		zh: [ "'''''Chinese'''''", "'''''Pinyin'''''" ],
		ko: [ "'''''Korean'''''", "'''''Romaja'''''" ],
		x: [ "'''''??'''''", "'''''Romanization'''''" ],
	},
	ulw: {
		en: [ '{{en-official}}' ],
		enx: [ '{{en-unofficial|1=<link to translation>}}' ],
		
		ja: [ '{{ja}}', '{{ja-r}}' ],
		zht: [ '{{zh-t}}', '{{zh-r}}' ],
		zhs: [ '{{zh-s}}', '{{zh-r}}' ],
		x: [ '{{head|??}}', '{{head|r}}' ],

		zh: [
			'<span class="error">Traditional (<code>zht</code>) or simplified (<code>zhs</code>)?</span>',
			'<span class="error">Traditional (<code>zht</code>) or simplified (<code>zhs</code>)?</span>'
		],
	},
}

function trim(text) {
	text = text.replace(/^\u3000/g, '＠＠'); // escape initial fullwidth space
	text = text.trim();
	text = text.replace(/^＠＠/g, '\u3000'); // restore initial fullwidth space
	return text;
}

function ei(id) {
	return document.getElementById(id);
}

function go() {
	let wiki = ei('wiki').value;
	let langOrig = ei('langOrig').value;
	let isOfficialEn = ei('isOfficialEn').checked;
	let s = {
		orig: trim(ei('textOrig').value),
		rom: trim(ei('textRom').value),
		eng: trim(ei('textEn').value),
	}
	let wikitable = [];
	let corresp = {}; // map original to romanization, save some keystrokes/copypasting
	
	for (let k in s) {
		s[k] = s[k].split('\n'); // turn each string into an array
		
		for (let i = 0; i < s[k].length; i++) {
			s[k][i] = trim(s[k][i]); // trim each string in our new array
		}
	}
	
	if (! headText[wiki][langOrig]) langOrig = 'x'; // fallback
	wikitable.push(tableHeadSyntax[wiki][0]);
	wikitable.push(tableHeadSyntax[wiki][1] + headText[wiki][langOrig][0]);
	if (s.rom[0] !== '') wikitable.push(tableHeadSyntax[wiki][1] + headText[wiki][langOrig][1]);
	if (s.eng[0] !== '') wikitable.push(tableHeadSyntax[wiki][1] + headText[wiki][(isOfficialEn ? 'en' : 'enx')][0]);
	
	for (let i = 0; i < s.orig.length; i++) {
		if (s.orig[i] === '') s.orig[i] = undefined;
		if (s.rom[i] === '') s.rom[i] = undefined;
		if (s.eng[i] === '') s.eng[i] = undefined;
		
		if (s.rom[i]) {
			s.rom[i] = s.rom[i].replace(/\s*;\s*/g, '\u3000'); // convert semicolon in romaji to fullwidth space
			s.rom[i] = s.rom[i].replace(/ +/g, ' '); // collapse consecutive plain spaces
		}
		
		if (! s.orig[i]) {
			s.orig[i] = br[wiki];
			s.rom[i] = false;
		} else if (s.orig[i] && s.orig[i].match(/^[^ぁ-ー㐀-鿕]+$/g) && (! s.rom[i] || s.rom[i] === s.orig[i])) {
			s.orig[i] = '{{shared}}|' + s.orig[i];
			s.rom[i] = false;
		} else if (! s.rom[i] && corresp[s.orig[i]]){
			s.rom[i] = corresp[s.orig[i]];
		} else if (s.rom[i]) {
			corresp[s.orig[i]] = s.rom[i]; // map original to romanization
		}
		
		s.orig[i] = ('\n' + '|' + s.orig[i]);
		s.rom[i] = (s.rom[i] ? ('\n' + '|' + s.rom[i]) : '');
		s.eng[i] = (s.eng[i] ? ('\n' + '|' + s.eng[i]) : '');

		wikitable.push('|-' + s.orig[i] + s.rom[i] + s.eng[i]);
	}
	
	wikitable.push('|}');
	
	ei('textOut').value = wikitable.join('\n');
}

function fillLanguagesDatalist() {
	ei('languages').innerText = null;
	
	let wiki = ei('wiki').value;
	
	for (let langCode in headText[wiki]) {
		let option = document.createElement("option");
		option.value = langCode;
		ei('languages').appendChild(option);
	}
}

function changeLanguageAttribute() {
	let lang = ei('langOrig').value;
	if (lang === '') lang = 'x';
	if (langIso[lang]) lang = langIso[lang];
	ei('textOrig').lang = lang;
	ei('textOut').lang = lang;
}

function toggleShowEn() {
	let temp = ! ei('showEn').checked;
	ei('setEn').hidden = temp;
	ei('isOfficialEn').hidden = temp;
	document.querySelector('label[for="isOfficialEn"]').hidden = temp;
}

function prepareAtWikiUrl() {
	let server = ei('atWikiServer').value;
	let page = ei('atWikiPageName').value;
	page = encodeURIComponent(page); // 🤷
	
	ei('atWikiUrl').value = `https://${server}/?cmd=backup&action=source&page=${page}&num=0`;
	console.log(ei('atWikiUrl').value);
}

function getAtWikiText() {
	ei('textOrig').value = '…';
	
	// 🙃
	fetch('https://allorigins.me/get?method=raw&url=' + encodeURIComponent(ei('atWikiUrl').value))
		.then(function(response) {
			return response.text()
				.then(function(text) {
					processAtWikiText(text);
				})
		})
}

function processAtWikiText(text) {
	let html = document.createElement('html');
	html.innerHTML = text;
	let pre = html.getElementsByClassName('cmd_backup');
	let lyrics;

	if (pre[0]) {
		// use sad regex to extract lyrics
		// [\S\s]: https://stackoverflow.com/a/1068308
		lyrics = pre[0].innerText.match(/\*\*歌詞([\S\s]+)\*\*コメント/);
		
		if (lyrics) {
			lyrics = lyrics[1];
			lyrics = lyrics.replace(/&bold\(\)\{(.*?)\}/g, '<b>$1</b>');
			lyrics = lyrics.replace(/&italic\(\)\{(.*?)\}/g, '<i>$1</i>');
			lyrics = lyrics.replace(/&u\(\)\{(.*?)\}/g, '<u>$1</u>');
			ei('atWikiForm').hidden = true;
		} else {
			lyrics = "Could not locate lyrics in wiki text."
		}
	} else {
		lyrics = "Could not locate wiki text."
	}
	
	ei('textOrig').value = trim(lyrics);
	go();
}

function prepare() {
	// Output is changed every time these change
	let temp = []
	
	temp = [
		ei('wiki'),
		ei('langOrig'),
		ei('isOfficialEn'),
		ei('textOrig'),
		ei('textRom'),
		ei('textEn'),
	]
	
	for (let i = 0; i < temp.length; i++) {
		temp[i].addEventListener("input", function() {
			go();
		})
	}
	
	ei('wiki').addEventListener("input", function() {
		fillLanguagesDatalist();
	})
	
	ei('langOrig').addEventListener("input", function() {
		changeLanguageAttribute();
	})
	
	ei('showEn').addEventListener("click", function() {
		toggleShowEn();
	})
	
	ei('atWikiStart').addEventListener("click", function() {
		ei("atWikiForm").hidden = false;
	})
	
	temp = [
		ei('atWikiServer'),
		ei('atWikiPageName'),
	]
	
	for (let i = 0; i < temp.length; i++) {
		temp[i].addEventListener("input", function() {
			prepareAtWikiUrl();
		})
	}
	
	ei('atWikiGo').addEventListener("click", function() {
		getAtWikiText();
	})
	
	fillLanguagesDatalist();
	changeLanguageAttribute();
	toggleShowEn();
}