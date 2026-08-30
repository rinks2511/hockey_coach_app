import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add CSS for Tabs
tab_css = """
    .nav-tabs { display: flex; gap: 4px; padding: 0 14px 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 12px; margin-top: 10px; }
    .nav-tab { background: transparent; color: #94a3b8; border: none; font-size: 0.85rem; font-weight: 700; padding: 8px 16px; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
    .nav-tab:hover { background: rgba(255,255,255,0.05); color: white; }
    .nav-tab.active { background: #38bdf8; color: #0b0f19; }
"""
content = content.replace("  </style>", tab_css + "\n  </style>")

# 2. Add Tab HTML and View Wrappers
tab_html = """
  <!-- TAB NAVIGATION -->
  <div class="nav-tabs">
    <button id="tab-tactics" onclick="switchTab('tactics')" class="nav-tab active">🛡️ Tactics Board</button>
    <button id="tab-subs" onclick="switchTab('subs')" class="nav-tab">⏱️ Substitution Planner</button>
  </div>

  <div id="view-tactics" style="display: block;">
  <div class="tactics-wrapper">
"""
content = content.replace("<div class=\"tactics-wrapper\" style=\"margin-top: 10px;\">", tab_html)

# 3. Extract the side-panel using regex to move it into view-subs
side_panel_match = re.search(r'(<div class="side-panel">.*?</div>\n\n  </div>)', content, re.DOTALL)
if side_panel_match:
    side_panel_html = side_panel_match.group(1)
    
    # Remove it from tactics-wrapper
    content = content.replace(side_panel_html, "  </div>\n</div>\n")
    
    # Now append the new view-subs right after view-tactics
    # Wait, side_panel_html has the closing `</div>` for `tactics-wrapper` at the end (the `\n\n  </div>`).
    # Let's clean it up.
    inner_side_panel = re.search(r'<div class="side-panel">(.*?)</div>\n\n  </div>', side_panel_html, re.DOTALL).group(1)
    
    view_subs_html = f"""
  <div id="view-subs" style="display: none; max-width: 800px; margin: 0 auto;">
    <div class="side-panel" style="width: 100%;">
      {inner_side_panel}
    </div>
  </div>
"""
    content = content.replace("  </div>\n</div>\n", "  </div>\n</div>\n" + view_subs_html)
    
# 4. Fix the CSS for tactics-wrapper to not have the 300px column anymore
content = content.replace("grid-template-columns: 1fr 300px;", "display: block; max-width: 900px; margin: 0 auto;")

# 5. Add switchTab function to JavaScript
switch_tab_js = """
  function switchTab(tab) {
    document.getElementById('view-tactics').style.display = tab === 'tactics' ? 'block' : 'none';
    document.getElementById('view-subs').style.display = tab === 'subs' ? 'block' : 'none';
    document.getElementById('tab-tactics').className = tab === 'tactics' ? 'nav-tab active' : 'nav-tab';
    document.getElementById('tab-subs').className = tab === 'subs' ? 'nav-tab active' : 'nav-tab';
  }
"""
content = content.replace("function toggleGoogleConfig() {", switch_tab_js + "\n  function toggleGoogleConfig() {")

with open('index.html', 'w') as f:
    f.write(content)

print("Tabs Implemented!")
