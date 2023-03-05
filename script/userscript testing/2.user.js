// ==UserScript==
// @name        TESTING 2
// @namespace   Violentmonkey Scripts
// @match       *://*/*
// @version     1.0
// @author      -
// @description -
// @grant       none
// @inject-into content
// ==/UserScript==

console.log(1, xa);
console.log(2, unsafeWindow.xa);

xa();
unsafeWindow.xa();