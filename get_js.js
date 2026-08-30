const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/<script>(.*?)<\/script>/s);
fs.writeFileSync('temp.js', match ? match[1] : '');
