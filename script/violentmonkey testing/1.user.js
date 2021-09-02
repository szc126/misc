// ==UserScript==
// @name        TESTING 1
// @namespace   Violentmonkey Scripts
// @match       *://*/*
// @version     1.0
// @author      -
// @description -
// @grant       none
// @inject-into content
// ==/UserScript==

console.log(unsafeWindow);

unsafeWindow.xa = function() {
	alert('xaa');
}
console.log('xa');

unsafeWindow.xb = 'xbb';
console.log('xb');

unsafeWindow.eval("window.xd = 'xdd';");

let xe = document.createElement('a');
xe.id = 'xee';
xe.xe = function() {
	alert('xee');
}
document.body.appendChild(xe);

let xf = document.createElement('script');
xf.innerHTML = `
	alert('xff');
`;
document.body.appendChild(xf);