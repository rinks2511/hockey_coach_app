  let currentLang = 'en';

  

  let squadLocal = null;
  try {
    const raw = localStorage.getItem('hv_myra_squad');
    if (raw) squadLocal = JSON.parse(raw);
  } catch (e) {
    console.error("Error parsing squad", e);
  }
  let squadPlayers = (squadLocal && Array.isArray(squadLocal) && squadLocal.length > 0) ? squadLocal : [
    "Sai Jiya", "Defne", "Shanaya", "Alina", "Liv", "Mira", "Hannah", "Kyra", "Kate", "Liz"
  ];


  let subMatrixState = {};

  function renderSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    squadPlayers.forEach((p, index) => {
      if (!subMatrixState[p]) {
        let defaultPlay = [true, true, true, true, true];
        subMatrixState[p] = defaultPlay;
      }
    });

    Object.keys(subMatrixState).forEach(p => {
      if (!squadPlayers.includes(p)) delete subMatrixState[p];
    });

    const gk = currentAssignments['gk'];
    const defenders = [currentAssignments['lb'], currentAssignments['cb'], currentAssignments['rb'], currentAssignments['sub_def']].filter(Boolean);
    const attackers = [currentAssignments['lm'], currentAssignments['cm'], currentAssignments['rm'], currentAssignments['st'], currentAssignments['sub_mid']].filter(Boolean);
    const unassigned = squadPlayers.filter(p => p !== gk && !defenders.includes(p) && !attackers.includes(p));

    const groupedPlayers = [];
    if (gk) groupedPlayers.push({ player: gk, label: 'GK' });
    defenders.forEach(p => groupedPlayers.push({ player: p, label: 'DEF' }));
    attackers.forEach(p => groupedPlayers.push({ player: p, label: 'MID/ATT' }));
    unassigned.forEach(p => groupedPlayers.push({ player: p, label: 'BENCH' }));

    groupedPlayers.forEach(item => {
      const player = item.player;
      if (subMatrixState[player]) {
        const tr = document.createElement('tr');
        
        // Add color coding based on position
        if (item.label === 'GK') tr.style.backgroundColor = '#1e3a8a';
        else if (item.label === 'DEF') tr.style.backgroundColor = '#064e3b';
        else if (item.label === 'MID/ATT') tr.style.backgroundColor = '#701a75';
        else tr.style.backgroundColor = '#3f3f46';
        
        const tdName = document.createElement('td');
        tdName.innerHTML = `<strong>${player}</strong> <span style="font-size:0.6rem; opacity:0.7;">(${item.label})</span>`;
        tdName.style.textAlign = 'left';
        tdName.style.paddingLeft = '10px';
        tr.appendChild(tdName);

        for (let i = 0; i < 5; i++) {
          const td = document.createElement('td');
          const cb = document.createElement('input');
          cb.type = 'checkbox';
          cb.className = 'sub-matrix-checkbox';
          cb.checked = subMatrixState[player][i];
          if (i === 0) cb.disabled = true; // Managed by tactics
          cb.onchange = (e) => {
            subMatrixState[player][i] = e.target.checked;
            validateSubstitutionMatrix();
          };
          td.appendChild(cb);
          tr.appendChild(td);
        }
        tbody.appendChild(tr);
      }
    });
    
    validateSubstitutionMatrix();
  }

  function validateSubstitutionMatrix() {
    const tbody = document.getElementById('subMatrixBody');
    const valMsg = document.getElementById('subMatrixValidation');
    if (!tbody) return;

    const rows = tbody.querySelectorAll('tr');
    let isValid = true;
    let errors = [];

    const colCounts = [0, 0, 0, 0, 0];
    Object.values(subMatrixState).forEach(checks => {
      checks.forEach((c, i) => { if (c) colCounts[i]++; });
    });

    const table = document.getElementById('subMatrixTable');
    for (let i = 0; i < 5; i++) {
      const isColValid = colCounts[i] === 8;
      table.querySelectorAll(`tr td:nth-child(${i+2}), th:nth-child(${i+2})`).forEach(cell => {
        if (!isColValid) cell.classList.add('invalid-col');
        else cell.classList.remove('invalid-col');
      });
      if (!isColValid) {
        isValid = false;
        errors.push(`Block ${i+1} needs exactly 8 players.`);
      }
    }

    // Row validation is relaxed because mathematically:
    // - GK plays 5 blocks
    // - 4 Defenders sharing 3 spots over 5 blocks means someone must play 3 blocks
    // - 5 Attackers sharing 4 spots over 5 blocks means everyone plays 4 blocks
    // We just ensure they don't play 0 blocks
    rows.forEach(tr => {
      const player = tr.querySelector('td').innerText;
      const count = subMatrixState[player] ? subMatrixState[player].filter(Boolean).length : 0;
      if (count === 0) {
        tr.classList.add('invalid-row');
        isValid = false;
        errors.push(`Player ${player} is playing 0 blocks.`);
      } else {
        tr.classList.remove('invalid-row');
      }
    });

    valMsg.innerText = isValid ? '' : errors.join(' ');
  }

  function switchTab(tab) {
    document.getElementById('view-tactics').style.display = tab === 'tactics' ? 'block' : 'none';
    document.getElementById('view-subs').style.display = tab === 'subs' ? 'block' : 'none';
    document.getElementById('tab-tactics').className = tab === 'tactics' ? 'nav-tab active' : 'nav-tab';
    document.getElementById('tab-subs').className = tab === 'subs' ? 'nav-tab active' : 'nav-tab';
  }

  let googleClientId = '1083993716124-rle31j9i93h345fg33o536o5ur6vmp6s.apps.googleusercontent.com';
  let coachEmails = JSON.parse(localStorage.getItem('hv_myra_coaches')) || ["singhalrajeev89@gmail.com"];
  let currentUserRole = 'parent';

  function toggleGoogleConfig() {
    const panel = document.getElementById('googleConfigPanel');
    if (panel) {
      panel.style.display = panel.style.display === 'none' ? 'flex' : 'none';
    }
  }

  function saveGoogleConfig() {
    const input = document.getElementById('googleClientIdInput');
    const val = input.value.trim();
    if (!val) {
      showToast('Please enter a valid Client ID');
      return;
    }
    localStorage.setItem('hv_myra_google_client_id', val);
    googleClientId = val;

    if (currentUserRole === 'coach') {
      const emailsInput = document.getElementById('coachEmailsInput');
      if (emailsInput) {
        const emailsVal = emailsInput.value.split(',')
          .map(e => e.trim().toLowerCase())
          .filter(e => e.length > 0);
        if (!emailsVal.includes('singhalrajeev89@gmail.com')) {
          emailsVal.push('singhalrajeev89@gmail.com');
        }
        coachEmails = emailsVal;
        localStorage.setItem('hv_myra_coaches', JSON.stringify(coachEmails));
      }
    }

    toggleGoogleConfig();
    initGoogleAuth();
    showToast('Configuration saved! Initializing...');
  }

  function determineUserRole(userEmail) {
    if (userEmail && coachEmails.includes(userEmail.toLowerCase())) {
      currentUserRole = 'coach';
    } else {
      currentUserRole = 'parent';
    }
    applyRolePrivileges();
  }

  function applyRolePrivileges() {
    const isCoach = (currentUserRole === 'coach');

    const badge = document.getElementById('roleBadge');
    if (badge) {
      if (isCoach) {
        badge.innerText = '👑 Coach';
        badge.style.backgroundColor = '#059669';
        badge.style.borderColor = '#10b981';
      } else {
        badge.innerText = '👪 Parent (Read-Only)';
        badge.style.backgroundColor = '#475569';
        badge.style.borderColor = '#64748b';
      }
    }

    const drawBtn = document.getElementById('modeDraw');
    const arrowBtn = document.getElementById('modeArrow');
    const eraserBtn = document.getElementById('modeEraser');
    const clearBtn = document.getElementById('btnResetLines');
    const form1 = document.getElementById('btnForm1');
    const form2 = document.getElementById('btnForm2');
    const form3 = document.getElementById('btnForm3');
    const saveBtn = document.getElementById('btnSave');
    const loadBtn = document.getElementById('btnLoad');
    const notes = document.getElementById('coachNotes');

    if (!isCoach) {
      setMode('select');
      if (drawBtn) drawBtn.disabled = true;
      if (arrowBtn) arrowBtn.disabled = true;
      if (eraserBtn) eraserBtn.disabled = true;
      if (clearBtn) clearBtn.disabled = true;
      if (form1) form1.disabled = true;
      if (form2) form2.disabled = true;
      if (form3) form3.disabled = true;
      if (saveBtn) saveBtn.style.display = 'none';
      if (loadBtn) loadBtn.style.display = 'none';
      if (notes) notes.readOnly = true;

      const squadTitle = document.getElementById('txtManageSquadTitle');
      const addPlayerDiv = document.querySelector('.add-player');
      if (squadTitle) squadTitle.style.display = 'none';
      if (addPlayerDiv) addPlayerDiv.style.display = 'none';

      document.querySelectorAll('.player-chip span').forEach(el => el.style.display = 'none');
    } else {
      if (drawBtn) drawBtn.disabled = false;
      if (arrowBtn) arrowBtn.disabled = false;
      if (eraserBtn) eraserBtn.disabled = false;
      if (clearBtn) clearBtn.disabled = false;
      if (form1) form1.disabled = false;
      if (form2) form2.disabled = false;
      if (form3) form3.disabled = false;
      if (saveBtn) saveBtn.style.display = 'inline-flex';
      if (loadBtn) loadBtn.style.display = 'inline-flex';
      if (notes) notes.readOnly = false;

      const squadTitle = document.getElementById('txtManageSquadTitle');
      const addPlayerDiv = document.querySelector('.add-player');
      if (squadTitle) squadTitle.style.display = 'block';
      if (addPlayerDiv) addPlayerDiv.style.display = 'flex';

      document.querySelectorAll('.player-chip span').forEach(el => el.style.display = 'inline');
    }

    document.querySelectorAll('.player-select-pill, .sidebar-select').forEach(select => {
      select.disabled = !isCoach;
    });

    const emailsGroup = document.getElementById('googleConfigEmailsGroup');
    if (emailsGroup) {
      emailsGroup.style.display = isCoach ? 'flex' : 'none';
    }
  }

  function saveGoogleConfigOverlay() {
    const input = document.getElementById('googleClientIdInputOverlay');
    const val = input.value.trim();
    if (!val) {
      showToast('Please enter a valid Client ID');
      return;
    }
    localStorage.setItem('hv_myra_google_client_id', val);
    googleClientId = val;
    initGoogleAuth();
    showToast('Client ID saved!');
  }

  function initGoogleAuth() {
    const overlay = document.getElementById('loginOverlay');
    if (!googleClientId) {
      if (overlay) overlay.style.display = 'flex';
      document.getElementById('googleAuthSetupOverlay').style.display = 'flex';
      document.getElementById('googleSignInButtonOverlay').style.display = 'none';
      currentUserRole = 'parent';
      applyRolePrivileges();
      return;
    }
    
    document.getElementById('googleAuthSetupOverlay').style.display = 'none';

    if (typeof google === 'undefined') {
      setTimeout(initGoogleAuth, 1000);
      return;
    }

    console.log("🚨🚨🚨 GOOGLE CLIENT ID BEING USED:", googleClientId, "🚨🚨🚨");
    google.accounts.id.initialize({
      client_id: googleClientId,
      callback: handleCredentialResponse
    });

    google.accounts.id.renderButton(
      document.getElementById("googleSignInButtonOverlay"),
      { theme: "filled_blue", size: "large", text: "signin_with", shape: "pill", width: 240 }
    );

    const localUser = localStorage.getItem('hv_myra_user');
    if (localUser) {
      if (overlay) overlay.style.display = 'none';
      showUserLoggedIn(JSON.parse(localUser));
    } else {
      currentUserRole = 'parent';
      applyRolePrivileges();
      if (overlay) overlay.style.display = 'flex';
      document.getElementById('googleSignInButtonOverlay').style.display = 'block';
      document.getElementById('googleUserProfile').style.display = 'none';
    }
  }

  function handleCredentialResponse(response) {
    const payload = decodeJwtResponse(response.credential);
    localStorage.setItem('hv_myra_user', JSON.stringify(payload));
    showUserLoggedIn(payload);
    showToast(`Welcome, ${payload.name}!`);
  }

  function decodeJwtResponse(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  }

  function showUserLoggedIn(user) {
    const overlay = document.getElementById('loginOverlay');
    if (overlay) overlay.style.display = 'none';
    
    document.getElementById('googleUserProfile').style.display = 'flex';
    document.getElementById('userAvatar').src = user.picture;
    document.getElementById('userName').innerText = user.given_name || user.name;

    determineUserRole(user.email);
  }

  function logoutGoogle() {
    localStorage.removeItem('hv_myra_user');
    document.getElementById('googleUserProfile').style.display = 'none';
    currentUserRole = 'parent';
    applyRolePrivileges();
    
    const overlay = document.getElementById('loginOverlay');
    if (overlay) overlay.style.display = 'flex';
    
    initGoogleAuth();
    showToast('Logged out');
  }

  

  function syncMatrixFromTactics() {
    if (typeof subMatrixState === 'undefined') return;
    
    // Initialize state for squad players if missing
    if (typeof squadPlayers !== 'undefined') {
      squadPlayers.forEach(p => {
        if (!subMatrixState[p]) {
          subMatrixState[p] = [true, true, true, true, true];
        }
      });
    }

    // First, clear the 0-6m block for everyone
    Object.keys(subMatrixState).forEach(p => subMatrixState[p][0] = false);
    
    // Then, set the 0-6m block for everyone on the pitch (excluding subs)
    const gkPlayer = currentAssignments['gk'];
    for (const [posId, p] of Object.entries(currentAssignments)) {
      if (posId === 'sub_def_att' || posId === 'sub_mid') continue;
      if (p && subMatrixState[p]) {
        subMatrixState[p][0] = true;
      }
    }
    
    // Lock GK for the whole match
    if (gkPlayer && subMatrixState[gkPlayer]) {
      for(let i=0; i<5; i++) subMatrixState[gkPlayer][i] = true;
    }
    
    renderSubstitutionMatrix();
  }

  function autoFillRotation() {
    // 1. Reset everything EXCEPT 0-6m and GK
    const gkPlayer = currentAssignments['gk'];
    squadPlayers.forEach(p => {
      if (!subMatrixState[p]) subMatrixState[p] = [false, false, false, false, false];
      if (p !== gkPlayer) {
         for(let i=1; i<5; i++) subMatrixState[p][i] = true; // Default everyone to PLAYING
      }
    });

    // 2. Define the exact players assigned to each position
    const ld = currentAssignments['ld'];
    const rd = currentAssignments['rd'];
    const lf = currentAssignments['lf'];
    const rf = currentAssignments['rf'];
    const sub_def_att = currentAssignments['sub_def_att'];
    
    const lm = currentAssignments['lm'];
    const cm = currentAssignments['cm'];
    const rm = currentAssignments['rm'];
    const sub_mid = currentAssignments['sub_mid'];

    // 3. Mathematical Rotation for Rest (unchecking players)
    // 0-6m is already synced: sub_def_att and sub_mid are resting.
    
    // 6-12m: Rest LD and LM
    if (ld && subMatrixState[ld]) subMatrixState[ld][1] = false;
    if (lm && subMatrixState[lm]) subMatrixState[lm][1] = false;

    // 12-18m: Rest RD and CM
    if (rd && subMatrixState[rd]) subMatrixState[rd][2] = false;
    if (cm && subMatrixState[cm]) subMatrixState[cm][2] = false;

    // 18-24m: Rest LF and RM
    if (lf && subMatrixState[lf]) subMatrixState[lf][3] = false;
    if (rm && subMatrixState[rm]) subMatrixState[rm][3] = false;

    // 24-30m: Rest RF and sub_mid
    if (rf && subMatrixState[rf]) subMatrixState[rf][4] = false;
    if (sub_mid && subMatrixState[sub_mid]) subMatrixState[sub_mid][4] = false;

    renderSubstitutionMatrix();
    showToast('Rotation Auto-Filled!');
  }

  function saveSquadLocal() {
    localStorage.setItem('hv_myra_squad', JSON.stringify(squadPlayers));
  }

  function renderSquadManager() {
    ['squadListContainer', 'squadListContainerSubs'].forEach(id => {
      const container = document.getElementById(id);
      if (!container) return;
      container.innerHTML = '';
      squadPlayers.forEach(player => {
        const chip = document.createElement('span');
        chip.className = 'player-chip';
        chip.style.cssText = 'background: #1c2230; padding: 2px 6px; border-radius: 10px; font-size: 0.65rem; display: inline-flex; align-items: center; gap: 4px; border: 1px solid #334155;';
        chip.innerHTML = `${player} <span onclick="deleteSquadPlayer('${player}')" style="color: #ef4444; cursor: pointer; font-weight: bold; padding: 0 2px;">&times;</span>`;
        container.appendChild(chip);
      });
    });
  }

  function addSquadPlayer(fromSubs = false) {
    const input = document.getElementById(fromSubs ? 'newPlayerInputSubs' : 'newPlayerInput');
    if (!input) return;
    const name = input.value.trim();
    if (!name) return;
    if (squadPlayers.includes(name)) {
      showToast('Player already in squad');
      return;
    }
    squadPlayers.push(name);
    input.value = '';
    saveSquadLocal();
    renderSquadManager();
    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();
    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();
    initDropdowns();
    showToast(`${name} added to squad`);
  }

  function deleteSquadPlayer(name) {
    if (squadPlayers.length <= 1) {
      showToast('Must have at least 1 player');
      return;
    }
    squadPlayers = squadPlayers.filter(p => p !== name);
    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();
    
    // Fallback if deleted player was assigned
    for (const [posId, assignedName] of Object.entries(currentAssignments)) {
      if (assignedName === name) {
        currentAssignments[posId] = squadPlayers[0] || '';
      }
    }
    
    saveSquadLocal();
    renderSquadManager();
    if (typeof renderSubstitutionMatrix === 'function') renderSubstitutionMatrix();
    initDropdowns();
    showToast(`${name} removed from squad`);
  }

  const positionDictionary = {
    gk: { en: { code: 'GK', label: 'GK (Goalkeeper)', circle: 'GK' }, nl: { code: 'K', label: 'K (Keeper)', circle: 'K' } },
    lb: { en: { code: 'LB', label: 'LB (Left Back)', circle: 'LB' }, nl: { code: 'LA', label: 'LA (Linksachter)', circle: 'LA' } },
    cb: { en: { code: 'CB', label: 'CB (Center Back)', circle: 'CB' }, nl: { code: 'CA', label: 'CA (Centraal Achter)', circle: 'CA' } },
    rb: { en: { code: 'RB', label: 'RB (Right Back)', circle: 'RB' }, nl: { code: 'RA', label: 'RA (Rechtsachter)', circle: 'RA' } },
    sub_def: { en: { code: 'SUB-DEF', label: 'SUB-DEF (Defense Sub)', circle: 'SUB<span class="sub-tag">DEF</span>' }, nl: { code: 'WISSEL-DEF', label: 'WISSEL-DEF', circle: 'WIS<span class="sub-tag">DEF</span>' } },
    lm: { en: { code: 'LM', label: 'LM (Left Midfield)', circle: 'LM' }, nl: { code: 'LM', label: 'LM (Linksmidden)', circle: 'LM' } },
    cm: { en: { code: 'CM', label: 'CM (Center Midfield)', circle: 'CM' }, nl: { code: 'CM', label: 'CM (Centraalmidden)', circle: 'CM' } },
    rm: { en: { code: 'RM', label: 'RM (Right Midfield)', circle: 'RM' }, nl: { code: 'RM', label: 'RM (Rechtsmidden)', circle: 'RM' } },
    sub_mid: { en: { code: 'SUB-MID', label: 'SUB-MID (Midfield Sub)', circle: 'SUB<span class="sub-tag">MID</span>' }, nl: { code: 'WISSEL-MID', label: 'WISSEL-MID', circle: 'WIS<span class="sub-tag">MID</span>' } },
    st: { en: { code: 'ST', label: 'ST (Striker / Forward)', circle: 'ST' }, nl: { code: 'SP', label: 'SP (Spits / Aanval)', circle: 'SP' } }
  };

  const positionsConfig = [
    { id: 'gk', default: 'Liz' },
    { id: 'ld', default: 'Liv' },
    { id: 'rd', default: 'Defne' },
    { id: 'lm', default: 'Kyra' },
    { id: 'cm', default: 'Mira' },
    { id: 'rm', default: 'Alina' },
    { id: 'lf', default: 'Kate' },
    { id: 'rf', default: 'Sai Jiya' },
    { id: 'sub_def_att', default: 'Hannah', isSubDef: true },
    { id: 'sub_mid', default: 'Shanaya', isSubMid: true }
  ];

  const rulesDictionary = {
    en: [
      { title: "🎯 15-Meter Flat Scoring Line", desc: "In 8v8 cross-pitch hockey, goals only count if the ball is hit or touched by an attacker <strong>past the straight 15-meter line</strong> into the goal." },
      { title: "🥅 Horizontal Cross-Pitch Format", desc: "Played across one half of a full hockey field (sideline to sideline). Teams play <strong>8 vs 8</strong> (1 Goalkeeper + 7 Outfield players)." },
      { title: "📏 5-Meter Distance Rule", desc: "Opponents must always keep at least <strong>5 meters distance</strong> on all free hits and side-ins. Self-passes are allowed immediately." },
      { title: "⏱️ Match Duration & Quarters", desc: "Played as <strong>4 x 15 minutes</strong> with 2-minute quarter breaks and a 5-minute half-time. Great for rotating all 10 players evenly." },
      { title: "🚫 Feet & Back of Stick (Bolle Kant)", desc: "Players may only play the ball with the <strong>flat side of the stick</strong>. Kicking or intentionally stopping the ball with feet/body is a foul." },
      { title: "⚠️ Dangerous Play & Safety", desc: "Slap shots and pushes are encouraged. Hard lifted balls or raising the stick above shoulder height near other players is forbidden." }
    ],
    nl: [
      { title: "🎯 15-Meter Doellijn (Geen Cirkel)", desc: "Bij 8-tallen op een half veld is er <strong>geen ronde cirkel</strong>. Een doelpunt telt alleen als de bal binnen of voorbij de <strong>rechte 15-meterlijn</strong> is geraakt door een aanvaller." },
      { title: "🥅 Dwars Veld (8 tegen 8)", desc: "Er wordt overdwars op een half veld gespeeld (van zijlijn tot zijlijn). Elk team speelt met <strong>8 spelers</strong> (1 Keeper + 7 Veldspelers)." },
      { title: "📏 5 Meter Afstand Houden", desc: "Tegenstanders moeten altijd minimaal <strong>5 meter afstand</strong> houden bij vrije slagen en inslaan. Zelfpass is direct toegestaan." },
      { title: "⏱️ Speeltijd & Kwartalen", desc: "De wedstrijd duurt <strong>4 x 15 minuten</strong> met 2 minuten rust tussen kwarten en 5 minuten rust halverwege." },
      { title: "🚫 Voet & Bolle Kant van de Stick", desc: "De bal mag alleen gespeeld worden met de <strong>platte kant van de stick</strong>. Afhouden of de bal met de voet stoppen is een overtreding." },
      { title: "⚠️ Veiligheid & Hoge Ballen", desc: "Schuifslag en flatsen worden aangemoedigd. Gevaarlijk hoog spelen of de stick boven schouderhoogte zwaaien bij tegenstanders is niet toegestaan." }
    ]
  };

  let currentAssignments = {};
  positionsConfig.forEach(p => currentAssignments[p.id] = p.default);

  const board = document.getElementById('board');
  const canvas = document.getElementById('drawCanvas');
  const ctx = canvas.getContext('2d');

  let currentMode = 'select';
  let isDrawing = false;
  let startX = 0, startY = 0;
  let snapshot = null;

  // Track drawn strokes so drawings scale and don't disappear on resize
  let drawnObjects = [];

  function resizeCanvas() {
    canvas.width = board.clientWidth;
    canvas.height = board.clientHeight;
    redrawCanvas();
  }
  window.addEventListener('resize', resizeCanvas);
  setTimeout(resizeCanvas, 100);

  function redrawCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawnObjects.forEach(item => {
      ctx.save();
      if (item.type === 'line') {
        ctx.strokeStyle = item.color;
        ctx.lineWidth = item.width;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.beginPath();
        item.points.forEach((pt, idx) => {
          const x = pt.x * canvas.width;
          const y = pt.y * canvas.height;
          if (idx === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.stroke();
      } else if (item.type === 'arrow') {
        const x1 = item.from.x * canvas.width;
        const y1 = item.from.y * canvas.height;
        const x2 = item.to.x * canvas.width;
        const y2 = item.to.y * canvas.height;
        drawArrowDirect(x1, y1, x2, y2, item.color, item.width);
      }
      ctx.restore();
    });
  }

  function formatDateForDisplay(isoDateString, lang) {
    if (!isoDateString) return "Saturday, 29 Aug 2026";
    const [year, month, day] = isoDateString.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    const targetLang = lang || currentLang;
    const options = { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' };
    return date.toLocaleDateString(targetLang === 'en' ? 'en-GB' : 'nl-NL', options);
  }

  function onDateSelected(isoValue) { syncBanner(); }

  function syncBanner() {
    document.getElementById('bannerMatchTitle').innerText = document.getElementById('matchOpponent').value || 'HV Myra O10 Match';
    const datePickerVal = document.getElementById('matchDatePicker').value;
    document.getElementById('bannerDate').innerText = '📅 ' + formatDateForDisplay(datePickerVal);
    document.getElementById('bannerQuarter').innerText = '⏱️ ' + (document.getElementById('matchQuarter').value || 'Lineup');
  }

  function setLanguage(lang) {
    currentLang = lang;
    document.getElementById('btnLangEN').classList.toggle('active', lang === 'en');
    document.getElementById('btnLangNL').classList.toggle('active', lang === 'nl');

    if (lang === 'en') {
      document.getElementById('svgPitchDefLine').textContent = "🛡️ Defending 15m Line";
      document.getElementById('svgPitchScoreLine').textContent = "🎯 Scoring Zone (15m)";
      document.getElementById('svgPitchDirection').textContent = "Attacking Direction ➔";
      document.getElementById('txtSideTitle').innerText = "Squad Lineup (10 Slots)";
      document.getElementById('txtNotesTitle').innerText = "Coach Match & Rotation Notes";
      document.getElementById('txtRulesHeader').innerText = "📖 KNHB Under 10 (O10) Match Rules & Guidelines";
    } else {
      document.getElementById('svgPitchDefLine').textContent = "🛡️ 15m Verdedigingslijn";
      document.getElementById('svgPitchScoreLine').textContent = "🎯 15m Doelgebied (Scoren)";
      document.getElementById('svgPitchDirection').textContent = "Aanvalsrichting ➔";
      document.getElementById('txtSideTitle').innerText = "Teamopstelling (10 Plekken)";
      document.getElementById('txtNotesTitle').innerText = "Coach Notities & Wisselschema";
      document.getElementById('txtRulesHeader').innerText = "📖 KNHB O10 Belangrijkste Spelregels";
    }

    renderPositionLabels();
    renderRules();
    syncBanner();
  }

  let customPositionNames = JSON.parse(localStorage.getItem('hv_myra_custom_positions')) || {};

  function getPositionDict(posId) {
    const base = positionDictionary[posId][currentLang];
    const custom = customPositionNames[posId] ? customPositionNames[posId][currentLang] : null;
    return custom ? { ...base, ...custom } : base;
  }

  function renamePosition(posId) {
    const currentDict = getPositionDict(posId);
    const newName = prompt(
      currentLang === 'en' 
        ? `Enter new label for ${currentDict.label || posId} (max 4 characters):` 
        : `Voer nieuwe afkorting in voor ${currentDict.label || posId} (max 4 tekens):`, 
      currentDict.code
    );
    if (newName === null) return;
    const cleanName = newName.trim().substring(0, 4);
    if (!cleanName) return;

    if (!customPositionNames[posId]) {
      customPositionNames[posId] = { en: {}, nl: {} };
    }
    
    customPositionNames[posId][currentLang] = { code: cleanName, circle: cleanName };
    const otherLang = currentLang === 'en' ? 'nl' : 'en';
    if (!customPositionNames[posId][otherLang]) {
      customPositionNames[posId][otherLang] = { code: cleanName, circle: cleanName };
    }

    localStorage.setItem('hv_myra_custom_positions', JSON.stringify(customPositionNames));
    renderPositionLabels();
    initDropdowns();
    showToast(`Position renamed to ${cleanName}`);
  }

  function renderPositionLabels() {
    positionsConfig.forEach(pos => {
      const dict = getPositionDict(pos.id);
      const circleEl = document.getElementById(`circle_${pos.id}`);
      if (circleEl) {
        if (pos.id === 'sub_def') {
          circleEl.innerHTML = `${dict.code.substring(0, 3)}<span class="sub-tag">DEF</span>`;
        } else if (pos.id === 'sub_mid') {
          circleEl.innerHTML = `${dict.code.substring(0, 3)}<span class="sub-tag">MID</span>`;
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
      row.className = 'position-row';
      const tagClass = pos.isSubDef ? 'pos-tag tag-sub-def' : (pos.isSubMid ? 'pos-tag tag-sub-mid' : 'pos-tag');
      row.innerHTML = `
        <span class="${tagClass}" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('${pos.id}')">${dict.code}</span>
        <select class="sidebar-select" id="select_side_${pos.id}" onchange="onPositionChanged('${pos.id}', this.value)">
          ${squadPlayers.map(player => `<option value="${player}">${player}</option>`).join('')}
        </select>
      `;
      sidebarContainer.appendChild(row);
      const sideSelect = document.getElementById(`select_side_${pos.id}`);
      if (sideSelect) sideSelect.value = currentAssignments[pos.id];
    });

    const oppMap = {
      'opp_gk': currentLang === 'en' ? 'GK' : 'K',
      'opp_lb': currentLang === 'en' ? 'LB' : 'LA',
      'opp_cb': currentLang === 'en' ? 'CB' : 'CA',
      'opp_rb': currentLang === 'en' ? 'RB' : 'RA',
      'opp_lm': 'LM', 'opp_cm': 'CM', 'opp_rm': 'RM',
      'opp_st': currentLang === 'en' ? 'ST' : 'SP'
    };
    for (const [id, code] of Object.entries(oppMap)) {
      const el = document.getElementById(id);
      if (el) el.querySelector('.token-circle').innerText = code;
    }
  }

  function renderRules() {
    const grid = document.getElementById('rulesGrid');
    grid.innerHTML = '';
    rulesDictionary[currentLang].forEach(r => {
      const card = document.createElement('div');
      card.className = 'rule-card';
      card.innerHTML = `<div class="rule-title">${r.title}</div><p>${r.desc}</p>`;
      grid.appendChild(card);
    });
  }

  function initDropdowns() {
    positionsConfig.forEach(pos => {
      const select = document.getElementById(`select_board_${pos.id}`);
      if (select) {
        select.innerHTML = '';
        squadPlayers.forEach(player => {
          const opt = document.createElement('option');
          opt.value = player;
          opt.innerText = player;
          select.appendChild(opt);
        });
        select.value = currentAssignments[pos.id];
      }
    });
    renderPositionLabels();
    renderRules();
  }

  function onPositionChanged(posId, selectedPlayer) {
    const previousPlayerAtThisPos = currentAssignments[posId];
    let otherPosWithThisPlayer = null;
    for (const [pId, pName] of Object.entries(currentAssignments)) {
      if (pId !== posId && pName === selectedPlayer) {
        otherPosWithThisPlayer = pId;
        break;
      }
    }

    currentAssignments[posId] = selectedPlayer;
    if (otherPosWithThisPlayer) {
      currentAssignments[otherPosWithThisPlayer] = previousPlayerAtThisPos;
    }

    positionsConfig.forEach(pos => {
      const boardSelect = document.getElementById(`select_board_${pos.id}`);
      const sideSelect = document.getElementById(`select_side_${pos.id}`);
      if (boardSelect) boardSelect.value = currentAssignments[pos.id];
      if (sideSelect) sideSelect.value = currentAssignments[pos.id];
    });
    
    saveTacticsLocal();
    if (typeof syncMatrixFromTactics === 'function') syncMatrixFromTactics();
  }

  /* Draggable Opponents & Ball */
  let activeElement = null;
  let offsetX = 0, offsetY = 0;

  function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => { toast.classList.remove('show'); }, 2000);
  }

  document.querySelectorAll('.draggable-token').forEach(el => {
    el.addEventListener('pointerdown', (e) => {
      if (currentMode !== 'select') return;
      if (currentUserRole !== 'coach') return; // Parents cannot drag
      if (e.target.tagName.toLowerCase() === 'select') return;
      activeElement = el;
      const rect = el.getBoundingClientRect();
      offsetX = e.clientX - (rect.left + rect.width / 2);
      offsetY = e.clientY - (rect.top + rect.height / 2);
      el.setPointerCapture(e.pointerId);
    });

    el.addEventListener('pointermove', (e) => {
      if (activeElement !== el) return;
      const boardRect = board.getBoundingClientRect();
      let x = e.clientX - boardRect.left - offsetX;
      let y = e.clientY - boardRect.top - offsetY;
      x = Math.max(15, Math.min(boardRect.width - 15, x));
      y = Math.max(15, Math.min(boardRect.height - 15, y));
      el.style.left = `${(x / boardRect.width) * 100}%`;
      el.style.top = `${(y / boardRect.height) * 100}%`;
    });

    el.addEventListener('pointerup', (e) => {
      if (activeElement === el) {
        el.releasePointerCapture(e.pointerId);
        activeElement = null;
      }
    });
  });

  /* -------------------------------------------------------------
     FIXED DRAWING & ERASER LOGIC (Robust, Point-to-Path, Erasable)
     ------------------------------------------------------------- */
  let currentStroke = [];

  function setMode(mode) {
    currentMode = mode;
    ['modeSelect', 'modeDraw', 'modeArrow', 'modeEraser'].forEach(id => {
      const btn = document.getElementById(id);
      if (btn) btn.classList.remove('active');
    });
    if (mode === 'select') document.getElementById('modeSelect').classList.add('active');
    if (mode === 'draw') document.getElementById('modeDraw').classList.add('active');
    if (mode === 'arrow') document.getElementById('modeArrow').classList.add('active');
    if (mode === 'eraser') document.getElementById('modeEraser').classList.add('active');

    // Pointer events activate whenever not in select mode
    canvas.style.pointerEvents = (mode === 'select') ? 'none' : 'all';
  }

  function getCanvasCoords(e) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: (e.clientX - rect.left),
      y: (e.clientY - rect.top),
      normX: (e.clientX - rect.left) / canvas.width,
      normY: (e.clientY - rect.top) / canvas.height
    };
  }

  canvas.addEventListener('pointerdown', (e) => {
    if (currentMode === 'select') return;
    if (currentUserRole !== 'coach') return; // Parents cannot draw!
    isDrawing = true;
    const coords = getCanvasCoords(e);
    startX = coords.x;
    startY = coords.y;

    if (currentMode === 'draw') {
      currentStroke = [{ x: coords.normX, y: coords.normY }];
      ctx.strokeStyle = '#facc15';
      ctx.lineWidth = 3.5;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.beginPath();
      ctx.moveTo(startX, startY);
    } else if (currentMode === 'arrow') {
      snapshot = ctx.getImageData(0, 0, canvas.width, canvas.height);
    } else if (currentMode === 'eraser') {
      eraseAtPoint(coords.normX, coords.normY);
    }
  });

  canvas.addEventListener('pointermove', (e) => {
    if (!isDrawing) return;
    const coords = getCanvasCoords(e);

    if (currentMode === 'draw') {
      currentStroke.push({ x: coords.normX, y: coords.normY });
      ctx.lineTo(coords.x, coords.y);
      ctx.stroke();
    } else if (currentMode === 'arrow') {
      if (snapshot) ctx.putImageData(snapshot, 0, 0);
      drawArrowDirect(startX, startY, coords.x, coords.y, '#38bdf8', 3.5);
    } else if (currentMode === 'eraser') {
      eraseAtPoint(coords.normX, coords.normY);
    }
  });

  canvas.addEventListener('pointerup', (e) => {
    if (!isDrawing) return;
    isDrawing = false;
    const coords = getCanvasCoords(e);

    if (currentMode === 'draw') {
      if (currentStroke.length > 1) {
        drawnObjects.push({
          type: 'line',
          color: '#facc15',
          width: 3.5,
          points: currentStroke
        });
      }
      currentStroke = [];
    } else if (currentMode === 'arrow') {
      drawnObjects.push({
        type: 'arrow',
        color: '#38bdf8',
        width: 3.5,
        from: { x: startX / canvas.width, y: startY / canvas.height },
        to: { x: coords.normX, y: coords.normY }
      });
      redrawCanvas();
    }
  });

  function drawArrowDirect(x1, y1, x2, y2, color, width) {
    const headlen = 14;
    const angle = Math.atan2(y2 - y1, x2 - x1);
    ctx.save();
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - headlen * Math.cos(angle - Math.PI / 6), y2 - headlen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(x2 - headlen * Math.cos(angle + Math.PI / 6), y2 - headlen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  // Erase closest stroke or segment on eraser touch
  function eraseAtPoint(normX, normY) {
    const threshold = 0.035; // Sensitivity radius
    let changed = false;

    drawnObjects = drawnObjects.filter(obj => {
      if (obj.type === 'line') {
        const nearPoint = obj.points.some(pt => {
          const dist = Math.hypot(pt.x - normX, pt.y - normY);
          return dist < threshold;
        });
        if (nearPoint) { changed = true; return false; }
      } else if (obj.type === 'arrow') {
        const distFrom = Math.hypot(obj.from.x - normX, obj.from.y - normY);
        const distTo = Math.hypot(obj.to.x - normX, obj.to.y - normY);
        if (distFrom < threshold || distTo < threshold) { changed = true; return false; }
      }
      return true;
    });

    if (changed) {
      redrawCanvas();
      showToast('Line Erased');
    }
  }

  function clearDrawings() {
    drawnObjects = [];
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    showToast('All Lines Cleared');
  }

  const formations = {
    '1-3-3-1': {
      'pos_gk': [6, 50], 'pos_lb': [23, 24], 'pos_cb': [20, 50], 'pos_rb': [23, 76], 'pos_sub_def': [12, 88],
      'pos_lm': [47, 26], 'pos_cm': [45, 50], 'pos_rm': [47, 74], 'pos_sub_mid': [32, 88], 'pos_st': [77, 50],
      'ball': [50, 50], 'opp_gk': [95, 50], 'opp_lb': [81, 26], 'opp_cb': [84, 50], 'opp_rb': [81, 74],
      'opp_lm': [56, 26], 'opp_cm': [55, 50], 'opp_rm': [56, 74], 'opp_st': [32, 50]
    },
    '1-3-1-2-1': {
      'pos_gk': [6, 50], 'pos_lb': [23, 24], 'pos_cb': [19, 50], 'pos_rb': [23, 76], 'pos_sub_def': [12, 88],
      'pos_cm': [40, 50], 'pos_lm': [58, 28], 'pos_rm': [58, 72], 'pos_sub_mid': [32, 88], 'pos_st': [80, 50],
      'ball': [50, 50], 'opp_gk': [95, 50], 'opp_lb': [81, 26], 'opp_cb': [84, 50], 'opp_rb': [81, 74],
      'opp_lm': [56, 28], 'opp_cm': [55, 50], 'opp_rm': [56, 72], 'opp_st': [32, 50]
    },
    '1-2-3-2': {
      'pos_gk': [6, 50], 'pos_lb': [22, 34], 'pos_cb': [17, 50], 'pos_rb': [22, 66], 'pos_sub_def': [12, 88],
      'pos_lm': [45, 22], 'pos_cm': [43, 50], 'pos_rm': [45, 78], 'pos_sub_mid': [32, 88], 'pos_st': [77, 40],
      'ball': [50, 48], 'opp_gk': [95, 50], 'opp_lb': [80, 26], 'opp_cb': [84, 50], 'opp_rb': [80, 74],
      'opp_lm': [55, 26], 'opp_cm': [54, 50], 'opp_rm': [55, 74], 'opp_st': [30, 50]
    }
  };

  function applyFormation(name) {
    const setup = formations[name];
    if (!setup) return;
    for (const [id, [left, top]] of Object.entries(setup)) {
      const el = document.getElementById(id);
      if (el) { el.style.left = `${left}%`; el.style.top = `${top}%`; }
    }
    showToast(`Applied Horizontal ${name}`);
  }

  function saveTacticsLocal() {
    const tokenPositions = {};
    document.querySelectorAll('.token').forEach(el => {
      tokenPositions[el.id] = {
        left: el.style.left,
        top: el.style.top
      };
    });

    const data = {
      assignments: currentAssignments,
      matchDate: document.getElementById('matchDatePicker').value,
      matchOpponent: document.getElementById('matchOpponent').value,
      matchQuarter: document.getElementById('matchQuarter').value,
      notes: document.getElementById('coachNotes').value,
      drawings: drawnObjects,
      tokenPositions: tokenPositions
    };
    localStorage.setItem('hv_myra_clean_pdf_board', JSON.stringify(data));
    showToast('Setup Saved!');
  }

  function loadTacticsLocal() {
    const raw = localStorage.getItem('hv_myra_clean_pdf_board');
    if (!raw) { alert('No saved setup found.'); return; }
    const data = JSON.parse(raw);
    if (data.assignments) currentAssignments = data.assignments;
    if (data.matchDate) document.getElementById('matchDatePicker').value = data.matchDate;
    if (data.matchOpponent) document.getElementById('matchOpponent').value = data.matchOpponent;
    if (data.matchQuarter) document.getElementById('matchQuarter').value = data.matchQuarter;
    if (data.notes) document.getElementById('coachNotes').value = data.notes;
    if (data.drawings) {
      drawnObjects = data.drawings;
      redrawCanvas();
    }
    if (data.tokenPositions) {
      for (const [id, pos] of Object.entries(data.tokenPositions)) {
        const el = document.getElementById(id);
        if (el) {
          el.style.left = pos.left;
          el.style.top = pos.top;
        }
      }
    }
    initDropdowns();
    syncBanner();
    showToast('Setup Loaded!');
    if (typeof syncMatrixFromTactics === 'function') syncMatrixFromTactics();
  }

  /* READ-ONLY HTML EXPORT: Clean, static, non-editable match sheet */
  function downloadReadOnlyHTML() {
    const datePickerVal = document.getElementById('matchDatePicker').value || '2026-08-29';
    const matchVal = document.getElementById('matchOpponent').value || 'HV Myra O10 Match';
    const quarterVal = document.getElementById('matchQuarter').value || 'Lineup';
    const dateFormatted = formatDateForDisplay(datePickerVal);
    const notes = document.getElementById('coachNotes').value;

    let tokensHTML = '';
    positionsConfig.forEach(pos => {
      const el = document.getElementById(`pos_${pos.id}`);
      const left = el.style.left;
      const top = el.style.top;
      const dict = getPositionDict(pos.id);
      const playerName = currentAssignments[pos.id];
      const typeClass = pos.id === 'gk' ? 'myra-gk' : (pos.isSubDef ? 'myra-sub-def' : (pos.isSubMid ? 'myra-sub-mid' : 'myra-field'));

      tokensHTML += `
        <div class="token ${typeClass}" style="position:absolute; top:${top}; left:${left}; transform:translate(-50%,-50%); display:flex; flex-direction:column; align-items:center;">
          <div class="token-circle">${dict.circle}</div>
          <div class="static-pill">${playerName}</div>
        </div>
      `;
    });

    const oppMap = {
      'opp_gk': { left: '95%', top: '50%', code: currentLang === 'en' ? 'GK' : 'K' },
      'opp_lb': { left: '81%', top: '26%', code: currentLang === 'en' ? 'LB' : 'LA' },
      'opp_cb': { left: '84%', top: '50%', code: currentLang === 'en' ? 'CB' : 'CA' },
      'opp_rb': { left: '81%', top: '74%', code: currentLang === 'en' ? 'RB' : 'RA' },
      'opp_lm': { left: '56%', top: '26%', code: 'LM' },
      'opp_cm': { left: '55%', top: '50%', code: 'CM' },
      'opp_rm': { left: '56%', top: '74%', code: 'RM' },
      'opp_st': { left: '32%', top: '50%', code: currentLang === 'en' ? 'ST' : 'SP' }
    };

    for (const [id, opp] of Object.entries(oppMap)) {
      tokensHTML += `
        <div class="token opp" style="position:absolute; top:${opp.top}; left:${opp.left}; transform:translate(-50%,-50%);">
          <div class="token-circle">${opp.code}</div>
        </div>
      `;
    }

    tokensHTML += `
      <div class="token ball" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);">
        <div class="token-circle" style="width:20px; height:20px; background:#fff; border:2px solid #1e293b; border-radius:50%;"></div>
      </div>
    `;

    let rosterRowsHTML = '';
    positionsConfig.forEach(pos => {
      const customEn = customPositionNames[pos.id] && customPositionNames[pos.id]['en'] ? customPositionNames[pos.id]['en'].code : positionDictionary[pos.id]['en'].code;
      const customNl = customPositionNames[pos.id] && customPositionNames[pos.id]['nl'] ? customPositionNames[pos.id]['nl'].code : positionDictionary[pos.id]['nl'].code;
      const enCode = customEn;
      const nlCode = customNl;
      const playerName = currentAssignments[pos.id];
      const tagColor = pos.isSubDef ? '#f59e0b' : (pos.isSubMid ? '#fb923c' : '#38bdf8');

      rosterRowsHTML += `
        <div class="roster-row">
          <span style="font-weight:800; color:${tagColor};">[${enCode} / ${nlCode}]</span>
          <span style="font-weight:700; color:#ffffff;">${playerName}</span>
        </div>
      `;
    });

    let rulesHTML = '';
    rulesDictionary[currentLang].forEach(r => {
      rulesHTML += `<div class="rule-card"><div class="rule-title">${r.title}</div><p>${r.desc}</p></div>`;
    });

    const readOnlyHTML = `<!DOCTYPE html>
<html lang="${currentLang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HV Myra O10 Match Sheet - ${datePickerVal}</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: #12161f; color: #eef4f8; padding: 12px; display: flex; justify-content: center; }
  .sheet-container { width: 100%; max-width: 1240px; display: flex; flex-direction: column; gap: 12px; }
  .header-bar { background: #1c2230; padding: 12px 18px; border-radius: 10px; border-left: 4px solid #f59e0b; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
  .header-title { font-size: 1.1rem; font-weight: 800; color: #fff; }
  .header-meta { font-size: 0.85rem; font-weight: 700; color: #f59e0b; display: flex; gap: 10px; }
  .main-grid { display: grid; grid-template-columns: 1fr 340px; gap: 12px; }
  @media (max-width: 900px) { .main-grid { grid-template-columns: 1fr; } }
  .board-container { position: relative; width: 100%; aspect-ratio: 1.55 / 1; background: #1f8a4c; border: 3px solid #ffffff; border-radius: 8px; overflow: hidden; }
  .token { position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center; transform: translate(-50%, -50%); }
  .token-circle { width: 36px; height: 36px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 800; font-size: 0.68rem; border: 2px solid white; line-height: 1; }
  .token.myra-field .token-circle { background: #003366; color: #ffffff; }
  .token.myra-gk .token-circle { background: #f59e0b; color: #000; }
  .token.myra-sub-def .token-circle { background: #d97706; color: #fff; border-color: #fde68a; }
  .token.myra-sub-mid .token-circle { background: #ea580c; color: #fff; border-color: #fed7aa; }
  .token.opp .token-circle { background: #c1121f; color: white; border-color: #fee2e2; }
  .static-pill { margin-top: 3px; background: rgba(9,13,20,0.95); color: #fff; border: 1px solid rgba(255,255,255,0.6); border-radius: 10px; font-size: 0.65rem; font-weight: 700; padding: 1.5px 6px; white-space: nowrap; }
  .side-card { background: #1c2230; padding: 12px; border-radius: 8px; display: flex; flex-direction: column; gap: 10px; }
  .card-title { font-size: 0.85rem; font-weight: 800; color: #38bdf8; border-bottom: 1px solid #334155; padding-bottom: 4px; }
  .roster-row { display: flex; justify-content: space-between; align-items: center; background: #0c1017; padding: 5px 8px; border-radius: 5px; font-size: 0.78rem; border: 1px solid #232c3d; }
  .notes-box { background: #0c1017; border: 1px solid #232c3d; border-radius: 5px; padding: 8px; font-size: 0.76rem; color: #cbd5e1; white-space: pre-wrap; line-height: 1.35; }
  .rules-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  @media (max-width: 900px) { .rules-grid { grid-template-columns: 1fr; } }
  .rule-card { background: #0c1017; border: 1px solid #232c3d; border-radius: 6px; padding: 8px 10px; }
  .rule-title { font-size: 0.76rem; font-weight: 700; color: #38bdf8; margin-bottom: 2px; }
  .rule-card p { font-size: 0.7rem; color: #cbd5e1; line-height: 1.3; }
  .legend-bar { display: flex; justify-content: center; gap: 14px; font-size: 0.75rem; color: #94a3b8; margin-top: 4px; flex-wrap: wrap; }

  .nav-tabs { display: flex; gap: 4px; padding: 0 14px 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 12px; margin-top: 10px; }
  .nav-tab { background: transparent; color: #94a3b8; border: none; font-size: 0.85rem; font-weight: 700; padding: 8px 16px; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
  .nav-tab:hover { background: rgba(255,255,255,0.05); color: white; }
  .nav-tab.active { background: #38bdf8; color: #0b0f19; }
  .sub-matrix-table { width: 100%; border-collapse: collapse; font-size: 0.75rem; color: white; background: #0c1017; border: 1px solid #232c3d; }
  .sub-matrix-table th, .sub-matrix-table td { border: 1px solid #232c3d; padding: 4px; text-align: center; }
  .sub-matrix-table th { background: #1e293b; color: #94a3b8; font-weight: 600; }
  .sub-matrix-table td:first-child { text-align: left; font-weight: bold; color: #38bdf8; max-width: 90px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .sub-matrix-checkbox { cursor: pointer; width: 14px; height: 14px; }
  .invalid-col { background: rgba(239, 68, 68, 0.2); }
  .invalid-row { background: rgba(239, 68, 68, 0.2); }

</style>
</head>
<body>
  <div class="sheet-container">
    <div class="header-bar">
      <div class="header-title">HV Myra O10 &bull; \${matchVal}</div>
      <div class="header-meta"><span>📅 \${dateFormatted}</span> <span>⏱️ \${quarterVal}</span></div>
    </div>
    <div class="main-grid">
      <div style="display:flex; flex-direction:column; gap:8px;">
        <div class="board-container">
          <svg style="position:absolute; top:0; left:0; width:100%; height:100%;" viewBox="0 0 1100 700" preserveAspectRatio="none">
            <rect x="0" y="0" width="1100" height="700" fill="none" stroke="#ffffff" stroke-width="4" />
            <rect x="0" y="270" width="22" height="160" fill="rgba(255,255,255,0.25)" stroke="#ffffff" stroke-width="3" />
            <rect x="1078" y="270" width="22" height="160" fill="rgba(255,255,255,0.25)" stroke="#ffffff" stroke-width="3" />
            <line x1="220" y1="0" x2="220" y2="700" stroke="#f59e0b" stroke-width="3" stroke-dasharray="10,8" />
            <rect x="12" y="12" width="170" height="22" fill="#090d14" rx="4" stroke="#f59e0b" stroke-width="1"/>
            <text x="18" y="27" fill="#f59e0b" font-size="11" font-weight="bold">\${currentLang === 'en' ? '🛡️ Defending 15m Line' : '🛡️ 15m Verdedigingslijn'}</text>
            <line x1="880" y1="0" x2="880" y2="700" stroke="#f59e0b" stroke-width="3" stroke-dasharray="10,8" />
            <rect x="918" y="12" width="170" height="22" fill="#090d14" rx="4" stroke="#f59e0b" stroke-width="1"/>
            <text x="924" y="27" fill="#f59e0b" font-size="11" font-weight="bold">\${currentLang === 'en' ? '🎯 Scoring Zone (15m)' : '🎯 15m Doelgebied (Scoren)'}</text>
            <rect x="880" y="0" width="220" height="700" fill="rgba(245,158,11,0.06)" />
            <line x1="550" y1="0" x2="550" y2="700" stroke="#ffffff" stroke-width="3" />
            <circle cx="550" cy="350" r="45" fill="none" stroke="#ffffff" stroke-width="2.5" />
            <circle cx="550" cy="350" r="4" fill="#ffffff" />
            <path d="M 460 665 L 640 665 M 625 655 L 640 665 L 625 675" fill="none" stroke="#38bdf8" stroke-width="2.5" />
            <text x="550" y="650" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">\${currentLang === 'en' ? 'Attacking Direction ➔' : 'Aanvalsrichting ➔'}</text>
          </svg>
          \${tokensHTML}
        </div>
        <div class="legend-bar">
          <span>🥅 Left: Myra Goal &bull; 🥅 Right: Opponent Goal &bull; 🎯 15m Line: Scoring Zone</span>
        </div>
      </div>
      <div class="side-card">
        <div class="card-title">Squad Lineup (10 Players)</div>
        <div style="display:flex; flex-direction:column; gap:4px;">
          \${rosterRowsHTML}
        </div>
        <div class="card-title" style="margin-top:6px;">Coach Match & Rotation Notes</div>
        <div class="notes-box">\${notes}</div>
      </div>
    </div>
    <div class="side-card" style="margin-top:4px;">
      <div class="card-title">📖 KNHB Under 10 (O10) Match Rules & Guidelines</div>
      <div class="rules-grid">
        \${rulesHTML}
      </div>
    </div>
  </div>
</body>
</html>`;

    const blob = new Blob([readOnlyHTML], { type: 'text/html;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `HV_Myra_O10_MatchSheet_\${datePickerVal}.html`;
    a.click();
    showToast('Read-Only Match HTML Downloaded!');
  }

  window.onload = () => {
    // Add showToast to fix missing declaration before use
    function showToast(message) {
      const toast = document.getElementById('toast');
      if(toast) {
        toast.innerText = message;
        toast.classList.add('show');
        setTimeout(() => { toast.classList.remove('show'); }, 2000);
      }
    }
    resizeCanvas();
    initDropdowns();
    renderSquadManager();
    if (typeof syncMatrixFromTactics === 'function') syncMatrixFromTactics();
    document.getElementById('googleClientIdInput').value = googleClientId;
    const overlayInput = document.getElementById('googleClientIdInputOverlay');
    if (overlayInput) {
      overlayInput.value = googleClientId;
    }
    const emailsInput = document.getElementById('coachEmailsInput');
    if (emailsInput) {
      emailsInput.value = coachEmails.join(', ');
    }
    initGoogleAuth();
    syncBanner();
  };
