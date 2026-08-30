import re

with open('index.html', 'r') as f:
    content = f.read()

old_load = """  function loadTacticsLocal() {
    const raw = localStorage.getItem('hv_myra_clean_pdf_board');
    if (!raw) { alert('No saved setup found.'); return; }
    const data = JSON.parse(raw);
    if (data.assignments) currentAssignments = data.assignments;"""

new_load = """  function loadTacticsLocal() {
    const raw = localStorage.getItem('hv_myra_clean_pdf_board');
    if (!raw) { alert('No saved setup found.'); return; }
    const data = JSON.parse(raw);
    if (data.assignments) {
      let a = data.assignments;
      // Migrate old 1-3-3-1 assignments to 1-2-3-2
      if (a.lb && !a.ld) a.ld = a.lb;
      if (a.cb && !a.rd) a.rd = a.cb;
      if (a.st && !a.lf) a.lf = a.st;
      if (a.rb && !a.rf) a.rf = a.rb;
      if (a.sub_def && !a.sub_def_att) a.sub_def_att = a.sub_def;
      currentAssignments = a;
    }"""

if old_load in content:
    content = content.replace(old_load, new_load)
    print("Fixed loadTacticsLocal")
else:
    print("WARNING: Could not find old_load")


# Also need to fix sync cloud tactics if it exists?
# The user clicked the "Load" button, which is `loadTacticsLocal`.
# Are there any other load functions?
old_cloud = """  async function loadTacticsFromCloud(revisionId) {
    if (!googleClientId) {
      alert("Please login via Google to load tactics.");
      return;
    }
    const token = getGoogleToken();
    if (!token) return;

    try {
      showToast('Loading from cloud...');
      const response = await fetch(`${API_URL}/tactics/${revisionId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        if (data.assignments) currentAssignments = data.assignments;"""

new_cloud = """  async function loadTacticsFromCloud(revisionId) {
    if (!googleClientId) {
      alert("Please login via Google to load tactics.");
      return;
    }
    const token = getGoogleToken();
    if (!token) return;

    try {
      showToast('Loading from cloud...');
      const response = await fetch(`${API_URL}/tactics/${revisionId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        if (data.assignments) {
          let a = data.assignments;
          // Migrate old 1-3-3-1 assignments to 1-2-3-2
          if (a.lb && !a.ld) a.ld = a.lb;
          if (a.cb && !a.rd) a.rd = a.cb;
          if (a.st && !a.lf) a.lf = a.st;
          if (a.rb && !a.rf) a.rf = a.rb;
          if (a.sub_def && !a.sub_def_att) a.sub_def_att = a.sub_def;
          currentAssignments = a;
        }"""

if old_cloud in content:
    content = content.replace(old_cloud, new_cloud)
    print("Fixed loadTacticsFromCloud")
else:
    print("Could not find loadTacticsFromCloud, skipping...")

with open('index.html', 'w') as f:
    f.write(content)
