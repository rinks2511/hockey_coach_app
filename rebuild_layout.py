import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Remove the incorrectly placed view-subs
view_subs_pattern = r'<div id="view-subs".*?<div class="coach-notes">.*?</div>\n    </div>\n  </div>\n'
content = re.sub(view_subs_pattern, '', content, flags=re.DOTALL)

# 2. Find the ACTUAL side-panel in tactics-wrapper
# It starts with <div class="side-panel"> and ends before the rules-panel or just at the end of tactics-wrapper.
# Let's extract it carefully.
side_panel_match = re.search(r'(<div class="side-panel">.*?</div>\n    </div>\n\n  </div>)', content, re.DOTALL)
if side_panel_match:
    original_side_panel = side_panel_match.group(1)
    # The inner content
    inner = re.search(r'<div class="side-panel">(.*?)</div>\n    </div>\n\n  </div>', original_side_panel, re.DOTALL).group(1)
    
    # We want to remove this side-panel from the tactics wrapper
    content = content.replace(original_side_panel, '  </div>\n')
    
    # And we create the proper view-subs at the correct location (after view-tactics closes)
    # The tactics-wrapper is inside view-tactics. Let's find where view-tactics closes.
    # Actually, view-tactics is just a div that wraps tactics-wrapper.
    # Wait, earlier I did:
    # content = content.replace("<div class=\"tactics-wrapper\" style=\"margin-top: 10px;\">", tab_html)
    # which output:
    # <div id="view-tactics" style="display: block;">
    # <div class="tactics-wrapper">
    
    # Let's close view-tactics after the rules-panel.
    rules_panel_end = content.find('</div>\n\n<div id="toast">Ready</div>')
    
    # Insert closing div for view-tactics and the new view-subs
    new_view_subs = f"""</div> <!-- end view-tactics -->

<div id="view-subs" style="display: none; max-width: 800px; margin: 0 auto; padding: 20px;">
  <div class="side-panel" style="width: 100%;">
    {inner}
  </div>
</div>
"""
    # Wait, we need to insert this exactly before <div id="toast">
    content = content.replace('</div>\n\n<div id="toast">Ready</div>', new_view_subs + '\n<div id="toast">Ready</div>')

# Fix tactics-wrapper CSS
content = content.replace("grid-template-columns: 1fr 300px;", "display: block; max-width: 900px; margin: 0 auto;")

with open('index.html', 'w') as f:
    f.write(content)

print("Rebuilt Layout")
