"use strict";

window.onload = function() {
	prepare();
	go(); // initialize stuff
}

let els = {
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

function go() {
	changeLanguageAttribute();
	
	let wiki = els.wiki.value;
	let langOrig = els.langOrig.value;
	let enIsOfficial = els.enType.checked;
	let s = {
		orig: trim(els.orig.value),
		rom: trim(els.rom.value),
		eng: trim(els.en.value),
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
	if (s.eng[0] !== '') wikitable.push(tableHeadSyntax[wiki][1] + headText[wiki][(enIsOfficial ? 'en' : 'enx')][1]);
	console.log(s);
	
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
	
	els.out.value = wikitable.join('\n');
}

function fillLanguagesDatalist() {
	
}

function changeLanguageAttribute() {
	let lang = els.langOrig.value;
	if (lang === '') lang = 'x';
	if (langIso[lang]) lang = langIso[lang];
	els.orig.lang = lang;
	els.out.lang = lang;
}

function prepare() {
	els.wiki = document.getElementById('wiki');
	els.langOrig = document.getElementById('langOrig');
	els.enType = document.getElementById('enType');
	els.orig = document.getElementById('textOrig');
	els.rom = document.getElementById('textRom');
	els.en = document.getElementById('textEn');
	els.out = document.getElementById('textOut');
	
	for (let elId in els) {
		if (elId === 'output') continue; // let people tamper with the output box
		
		els[elId].addEventListener("input", function() {
			go();
		})
	}
	
	document.getElementById('showEn').addEventListener("click", function() {
		document.getElementById('setEn').hidden = ! this.checked;
	})
}