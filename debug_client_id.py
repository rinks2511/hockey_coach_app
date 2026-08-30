import re

with open('index.html', 'r') as f:
    content = f.read()

# Add a console.log right before google.accounts.id.initialize
old_init = """    google.accounts.id.initialize({
      client_id: googleClientId,
      callback: handleCredentialResponse
    });"""

new_init = """    console.log("🚨🚨🚨 GOOGLE CLIENT ID BEING USED:", googleClientId, "🚨🚨🚨");
    google.accounts.id.initialize({
      client_id: googleClientId,
      callback: handleCredentialResponse
    });"""

content = content.replace(old_init, new_init)

with open('index.html', 'w') as f:
    f.write(content)
