const { JSDOM } = require("jsdom");
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const dom = new JSDOM(html, { 
  url: "http://localhost/", 
  runScripts: "dangerously" 
});
const window = dom.window;

setTimeout(() => {
  try {
    console.log("Before: ", window.document.getElementById('pos_p1').style.left);
    window.applyFormation('1-3-3-1');
    console.log("After 1-3-3-1: ", window.document.getElementById('pos_p1').style.left);
    window.applyFormation('1-2-4-1');
    console.log("After 1-2-4-1: ", window.document.getElementById('pos_p1').style.left);
    
    window.setLanguage('nl');
    console.log("After setLanguage nl: ", window.document.getElementById('circle_p1').innerHTML);
  } catch (e) {
    console.error("Error clicking:", e);
  }
}, 500);
