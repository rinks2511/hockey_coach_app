const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// 1. Fix dangling brackets syntax error in applyFormation
html = html.replace(/\}\n    \}\n    showToast\(`Applied Horizontal \$\{name\}`\);\n  \}/g, '}');

// 2. Fix the else else syntax error
html = html.replace(/\s*\} else \{\n\s*\/\/ If we did load, maybe we shouldn't overwrite. But wait, local load is done manually via loadTacticsLocal\(\)\n\s*\/\/ Let's just apply it by default so it looks right on fresh load\n\s*applyFormation\('1-2-3-2'\);\n\s*\}/g, '');
html = html.replace(/loadMatchData\(JSON\.parse\(rawData\)\);\n  \};/g, "loadMatchData(JSON.parse(rawData));\n    }\n  };");

// 3. Replace renderPositionLabels properly (using exact string matching instead of regex)
const oldRender = `  function renderPositionLabels() {
    positionsConfig.forEach(pos => {
      const dict = getPositionDict(pos.id);
      const circleEl = document.getElementById(\`circle_\${pos.id}\`);
      if (circleEl) {
        if (pos.id === 'sub_def') {
          circleEl.innerHTML = \`\${dict.code.substring(0, 3)}<span class="sub-tag">DEF</span>\`;
        } else if (pos.id === 'sub_mid') {
          circleEl.innerHTML = \`\${dict.code.substring(0, 3)}<span class="sub-tag">MID</span>\`;
        } else {
          circleEl.innerHTML = dict.circle;
        }
      }
    });

    const sidebarContainer = document.getElementById('sidebarPositionsList');
    sidebarContainer.innerHTML = '';
    positionsConfig.forEach(pos => {
      const dict = getPositionDict(pos.id);
      const row = document.createElement('div');
      row.className = 'squad-row';
      row.innerHTML = \`
        <span id="lbl_side_\${pos.id}" style="font-weight: bold; width: 60px; font-size: 0.8rem; color: #38bdf8;">\${dict.code}</span>
        <select class="player-select" id="select_side_\${pos.id}" onchange="onPositionChanged('\${pos.id}', this.value)">
          <option value="">--</option>
        </select>
      \`;
      sidebarContainer.appendChild(row);
    });
  }`;

const newRender = `  function renderPositionLabels() {
    positionsConfig.forEach(pos => {
      const circleEl = document.getElementById(\`circle_\${pos.id}\`);
      const tokenEl = document.getElementById(\`pos_\${pos.id}\`);
      let label = "";
      
      if (pos.id === 'sub_def') {
        label = currentLang === 'en' ? 'SUB<span class="sub-tag">DEF</span>' : 'WIS<span class="sub-tag">DEF</span>';
        if (circleEl) circleEl.innerHTML = label;
      } else if (pos.id === 'sub_mid') {
        label = currentLang === 'en' ? 'SUB<span class="sub-tag">MID</span>' : 'WIS<span class="sub-tag">MID</span>';
        if (circleEl) circleEl.innerHTML = label;
      } else {
        if (tokenEl) label = tokenEl.getAttribute('data-pos') || pos.id.toUpperCase();
        if (circleEl) circleEl.innerHTML = label;
      }
    });

    const sidebarContainer = document.getElementById('sidebarPositionsList');
    sidebarContainer.innerHTML = '';
    positionsConfig.forEach(pos => {
      const tokenEl = document.getElementById(\`pos_\${pos.id}\`);
      let label = "";
      if (pos.id === 'sub_def') {
        label = currentLang === 'en' ? 'SUB-DEF' : 'WIS-DEF';
      } else if (pos.id === 'sub_mid') {
        label = currentLang === 'en' ? 'SUB-MID' : 'WIS-MID';
      } else {
        label = tokenEl ? tokenEl.getAttribute('data-pos') : pos.id.toUpperCase();
      }

      const row = document.createElement('div');
      row.className = 'squad-row';
      row.innerHTML = \`
        <span id="lbl_side_\${pos.id}" style="font-weight: bold; width: 60px; font-size: 0.8rem; color: #38bdf8;">\${label}</span>
        <select class="player-select" id="select_side_\${pos.id}" onchange="onPositionChanged('\${pos.id}', this.value)">
          <option value="">--</option>
        </select>
      \`;
      sidebarContainer.appendChild(row);
    });
  }`;

html = html.replace(oldRender, newRender);

// Fix setLanguage missing initDropdowns
html = html.replace("    renderPositionLabels();\n    renderRules();", "    renderPositionLabels();\n    initDropdowns();\n    renderRules();");

fs.writeFileSync('index.html', html);
console.log("Fixed all bugs");
