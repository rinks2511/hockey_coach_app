import re

with open('index.html', 'r') as f:
    content = f.read()

# Remove the line that forces deleting the client ID
content = content.replace("localStorage.removeItem('hv_myra_google_client_id');", "")

# Update let googleClientId to read from localStorage FIRST
old_client_id = "let googleClientId = '1083993716124-rle31j9i93h345fg33o53605ur6vmp6s.apps.googleusercontent.com';"
new_client_id = "let googleClientId = localStorage.getItem('hv_myra_google_client_id') || '1083993716124-rle31j9i93h345fg33o53605ur6vmp6s.apps.googleusercontent.com';"
content = content.replace(old_client_id, new_client_id)

with open('index.html', 'w') as f:
    f.write(content)
print("Fixed Google Auth localStorage bug")
