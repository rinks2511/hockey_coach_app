import re

# Update index.html
with open('index.html', 'r') as f:
    content = f.read()

content = content.replace('<label id="lblMatchQuarter">⏱️ Period / Quarter</label>', '<label id="lblMatchHalf">⏱️ Match Half</label>')
content = content.replace('id="matchQuarter"', 'id="matchHalf"')
content = content.replace('value="Q1 Lineup"', 'value="1st Half Lineup"')
content = content.replace('id="bannerQuarter"', 'id="bannerHalf"')
content = content.replace('⏱️ Q1 Lineup', '⏱️ 1st Half Lineup')

# Rules text
old_rule = 'Played as <strong>4 x 15 minutes</strong> with 2-minute quarter breaks and a 5-minute half-time. Great for rotating all 10 players evenly.'
new_rule = 'Played as <strong>2 halves</strong> of 25-30 minutes with a 5-minute half-time. Great for rotating all 10 players.'
content = content.replace(old_rule, new_rule)

# syncBanner
content = content.replace("document.getElementById('bannerQuarter').innerText = '⏱️ ' + (document.getElementById('matchQuarter').value || 'Lineup');", 
                          "document.getElementById('bannerHalf').innerText = '⏱️ ' + (document.getElementById('matchHalf').value || 'Lineup');")

# saveTacticsLocal
content = content.replace('matchQuarter: document.getElementById(\'matchQuarter\').value,', 'matchHalf: document.getElementById(\'matchHalf\').value,')

# loadTacticsLocal
content = content.replace("if (data.matchQuarter) document.getElementById('matchQuarter').value = data.matchQuarter;", 
                          "if (data.matchHalf) document.getElementById('matchHalf').value = data.matchHalf;")

# download read-only HTML
content = content.replace("const quarterVal = document.getElementById('matchQuarter').value || 'Lineup';",
                          "const quarterVal = document.getElementById('matchHalf').value || 'Lineup';")

with open('index.html', 'w') as f:
    f.write(content)

# Update rules.md
with open('docs/rules.md', 'r') as f:
    content = f.read()

content = content.replace('## 4. ⏱️ Match Duration & Quarters', '## 4. ⏱️ Match Duration & Halves')
content = content.replace('Matches are played as **4 x 15 minutes** with 2-minute quarter breaks and a 5-minute half-time. This provides a great opportunity to rotate all 10 players evenly.',
                          'Matches are played as **2 halves** with a 5-minute half-time. This provides a great opportunity to rotate all 10 players.')
with open('docs/rules.md', 'w') as f:
    f.write(content)

