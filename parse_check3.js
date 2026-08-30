const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const { JSDOM } = require("jsdom");
const dom = new JSDOM(html);
const document = dom.window.document;
const tbodys = document.querySelectorAll('#subMatrixBody');
console.log("Found tbodys in DOM: ", tbodys.length);
if (tbodys.length > 0) {
  let node = tbodys[0];
  while (node && node.tagName !== 'BODY') {
    console.log(node.tagName, node.id, node.className);
    node = node.parentElement;
  }
}
