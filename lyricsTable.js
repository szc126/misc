let wikiDropdown = undefined;
let origLangBox = undefined;
let origBox = undefined;
let romBox = undefined;
let engBox = undefined;
let outputBox = undefined;

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

let headText = {
	vw: {
		en: "foobar",
		
		ja: [ "''Japanese'' (日本語歌詞)", "''Romaji'' (ローマ字)" ],
		zht: [ "''Chinese'' (中文歌詞)", "''Pinyin'' (拼音)" ],
		zhs: [ "''Chinese'' (中文歌词)", "''Pinyin'' (拼音)" ],
		ko: [ "''Korean'' (한국어 가사)", "''Romaja'' (로마자)" ],
		yuet: [ "''Cantonese'' (廣東話歌詞)", "''Jyutping'' (粵拼)" ],
		yues: [ "''Cantonese'' (广东话歌词)", "''Jyutping'' (粤拼)" ],

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
		en: "'''''English'''''",
		
		ja: [ "'''''Japanese'''''", "'''''Romaji'''''" ],
	},
	ulw: {
		enx: '{{en-unofficial}}',
		eno: '{{en-official}}',
		
		ja: [ '{{ja}}', '{{ja-r}}' ],
	},
}

function trim(text) {
	text = text.replace(/^\u3000/g, '＠＠'); // escape initial fullwidth space
	text = text.trim();
	text = text.replace(/^＠＠/g, '\u3000'); // restore initial fullwidth space
	return text;
}

function go() {
	let wiki = wikiDropdown.options[wikiDropdown.selectedIndex].value;
	let origLang = origLangBox.value;
	let s = {
		orig: trim(origBox.value),
		rom: trim(romBox.value),
		eng: trim(engBox.value),
	}
	let wikitable = [];
	
	for (var k in s) {
		s[k] = s[k].split('\n'); // turn each string into an array
		
		for (var i = 0; i < s[k].length; i++) {
			s[k][i] = trim(s[k][i]); // trim each string in our new array
		}
	}
	
	wikitable.push(tableHeadSyntax[wiki][0]);
	wikitable.push(tableHeadSyntax[wiki][1] + headText[wiki][origLang][0]);
	wikitable.push(tableHeadSyntax[wiki][1] + headText[wiki][origLang][1]);
	
	for (var i = 0; i < s.orig.length; i++) {
		if (s.rom[i]) s.rom[i] = s.rom[i].replace(/;/g, '\u3000'); // convert semicolon in romaji to fullwidth space
		
		if (s.orig[i] === '' && s.rom[i] === '') {
			s.orig[i] = br[wiki];
			s.rom[i] = false;
		} else if (s.orig[i].match(/^[^ぁ-ー㐀-鿕]+$/g) && (s.rom[i] === '' || s.rom[i] === s.orig[i])) {
			s.orig[i] = '{{shared}}|' + s.orig[i];
			s.rom[i] = false;
		}
		
		s.orig[i] = ('\n' + '|' + s.orig[i]);
		s.rom[i] = (s.rom[i] ? ('\n' + '|' + s.rom[i]) : '');
		s.eng[i] = (s.eng[i] ? ('\n' + '|' + s.eng[i]) : '');

		wikitable.push('|-' + s.orig[i] + s.rom[i] + s.eng[i]);
	}
	
	wikitable.push('|}');
	
	outputBox.innerHTML = wikitable.join('\n');
}

function main() {
	let els = document.querySelectorAll('[id]');
	
	wikiDropdown = document.getElementById("wiki");
	origLangBox = document.getElementById("language");
	origBox = document.getElementById("original");
	romBox = document.getElementById("romanization");
	engBox = document.getElementById("english");
	outputBox = document.getElementById("output");
	
	for (var i = 0; i < els.length; i++) {
		els[i].oninput = function() {
			go();
		}
	}
}

document.addEventListener(
	'DOMContentLoaded',
	function() {
		main();
	},
	false
);