// ==UserScript==
// @name        TESTING 3 iterable
// @namespace   Violentmonkey Scripts
// @match       *://*/*
// @grant       none
// @version     1.0
// @author      -
// @description -
// ==/UserScript==

let temp;

temp = new URLSearchParams(window.location.search);
console.log(1, window.location.search, temp, temp.toString());
for (let pair of temp.entries()) {
	console.log(pair);
}