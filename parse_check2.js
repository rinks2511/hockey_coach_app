const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const { JSDOM } = require("jsdom");
const dom = new JSDOM(html);
const document = dom.window.document;
const tbodys = document.querySelectorAll('#subMatrixBody');
console.log("Found tbodys in DOM: ", tbodys.length);
if (tbodys.length > 0) {
  console.log("Tbody 1 parent: ", tbodys[0].parentElement.parentElement.parentElement.id);
}
