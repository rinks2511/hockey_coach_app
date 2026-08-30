import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Update buttons
btn_pattern = r'<button onclick="applyFormation\(\'1-2-3-2\'\)".*?</div>'
btn_replace = """<button onclick="applyFormation('1-2-3-2')" id="btnForm1" class="active">1-2-3-2 (Standard)</button>
      <button onclick="applyFormation('1-3-3-1')" id="btnForm2">1-3-3-1 (Defensive)</button>
      <button onclick="applyFormation('1-2-4-1')" id="btnForm3">1-2-4-1 (Possession)</button>
      <button onclick="applyFormation('1-1-3-3')" id="btnForm4">1-1-3-3 (Attack)</button>
    </div>"""
content = re.sub(btn_pattern, btn_replace, content, flags=re.DOTALL)

# 2. Refactor tokens (Myra)
tokens = [("lb", "p1"), ("ls", "p2"), ("rb", "p3"), ("lm", "p4"), ("cm", "p5"), ("rm", "p6"), ("rs", "p7")]
for old, new in tokens:
    content = content.replace(f'id="pos_{old}"', f'id="pos_{new}"')
    content = content.replace(f'data-pos="{old.upper()}"', f'data-pos="P"')
    content = content.replace(f'id="circle_{old}"', f'id="circle_{new}"')
    content = content.replace(f"renamePosition('{old}')", f"renamePosition('{new}')")
    content = content.replace(f'id="select_board_{old}"', f'id="select_board_{new}"')
    content = content.replace(f"onPositionChanged('{old}', this.value)", f"onPositionChanged('{new}', this.value)")
    content = content.replace(f'id="lbl_side_{old}"', f'id="lbl_side_{new}"')

# 3. Refactor opponents
for old, new in tokens:
    content = content.replace(f'id="opp_{old}"', f'id="opp_{new}"')

# 4. Dictionary and Config
dict_pattern = r'const positionDictionary = \{.*?\};'
new_dict = """const positionDictionary = {
    gk: { en: { code: 'GK', label: 'GK (Goalkeeper)', circle: 'GK' }, nl: { code: 'K', label: 'K (Keeper)', circle: 'K' } },
    p1: { en: { code: 'P1', label: 'P1', circle: 'P1' }, nl: { code: 'P1', label: 'P1', circle: 'P1' } },
    p2: { en: { code: 'P2', label: 'P2', circle: 'P2' }, nl: { code: 'P2', label: 'P2', circle: 'P2' } },
    p3: { en: { code: 'P3', label: 'P3', circle: 'P3' }, nl: { code: 'P3', label: 'P3', circle: 'P3' } },
    p4: { en: { code: 'P4', label: 'P4', circle: 'P4' }, nl: { code: 'P4', label: 'P4', circle: 'P4' } },
    p5: { en: { code: 'P5', label: 'P5', circle: 'P5' }, nl: { code: 'P5', label: 'P5', circle: 'P5' } },
    p6: { en: { code: 'P6', label: 'P6', circle: 'P6' }, nl: { code: 'P6', label: 'P6', circle: 'P6' } },
    p7: { en: { code: 'P7', label: 'P7', circle: 'P7' }, nl: { code: 'P7', label: 'P7', circle: 'P7' } },
    sub_def: { en: { code: 'SUB-DEF', label: 'SUB-DEF (Defense Sub)', circle: 'SUB<span class="sub-tag">DEF</span>' }, nl: { code: 'WISSEL-DEF', label: 'WISSEL-DEF', circle: 'WIS<span class="sub-tag">DEF</span>' } },
    sub_mid: { en: { code: 'SUB-MID', label: 'SUB-MID (Midfield Sub)', circle: 'SUB<span class="sub-tag">MID</span>' }, nl: { code: 'WISSEL-MID', label: 'WISSEL-MID', circle: 'WIS<span class="sub-tag">MID</span>' } }
  };"""
content = re.sub(dict_pattern, new_dict, content, flags=re.DOTALL)

config_pattern = r'const positionsConfig = \[.*?\];'
new_config = """const positionsConfig = [
    { id: 'gk', default: 'Liz' },
    { id: 'p1', default: 'Liv' },
    { id: 'p2', default: 'Defne' },
    { id: 'p3', default: 'Sai Jiya' },
    { id: 'sub_def', default: 'Hannah', isSubDef: true },
    { id: 'p4', default: 'Kyra' },
    { id: 'p5', default: 'Mira' },
    { id: 'p6', default: 'Alina' },
    { id: 'sub_mid', default: 'Shanaya', isSubMid: true },
    { id: 'p7', default: 'Kate' }
  ];"""
content = re.sub(config_pattern, new_config, content, flags=re.DOTALL)

# 5. Replace Formations Dictionary completely
formations_pattern = r"const formations = \{.*?\n  \};\n\n  function applyFormation"
new_formations = """const formations = {
    '1-2-3-2': {
      name: '1-2-3-2 (Standard)',
      'pos_gk': { left: 6, top: 50, role: 'GK' }, 
      'pos_p1': { left: 22, top: 34, role: 'LB' }, 
      'pos_p2': { left: 77, top: 34, role: 'LS' }, 
      'pos_p3': { left: 22, top: 66, role: 'RB' }, 
      'pos_p4': { left: 45, top: 22, role: 'LM' }, 
      'pos_p5': { left: 43, top: 50, role: 'CM' }, 
      'pos_p6': { left: 45, top: 78, role: 'RM' }, 
      'pos_p7': { left: 77, top: 66, role: 'RS' },
      'pos_sub_def': { left: 12, top: 88, role: 'SUB' },
      'pos_sub_mid': { left: 32, top: 88, role: 'SUB' },
      'ball': { left: 50, top: 48, role: 'BALL' }, 
      'opp_gk': { left: 95, top: 50, role: 'GK' }, 
      'opp_p1': { left: 80, top: 26, role: 'LB' }, 
      'opp_p2': { left: 30, top: 34, role: 'LS' }, 
      'opp_p3': { left: 80, top: 74, role: 'RB' }, 
      'opp_p4': { left: 55, top: 26, role: 'LM' }, 
      'opp_p5': { left: 54, top: 50, role: 'CM' }, 
      'opp_p6': { left: 55, top: 74, role: 'RM' }, 
      'opp_p7': { left: 30, top: 66, role: 'RS' }
    },
    '1-3-3-1': {
      name: '1-3-3-1 (Defensive)',
      'pos_gk': { left: 6, top: 50, role: 'GK' },
      'pos_p1': { left: 23, top: 24, role: 'LB' },
      'pos_p2': { left: 20, top: 50, role: 'CB' },
      'pos_p3': { left: 23, top: 76, role: 'RB' },
      'pos_p4': { left: 47, top: 26, role: 'LM' },
      'pos_p5': { left: 45, top: 50, role: 'CM' },
      'pos_p6': { left: 47, top: 74, role: 'RM' },
      'pos_p7': { left: 77, top: 50, role: 'ST' },
      'pos_sub_def': { left: 12, top: 88, role: 'SUB' },
      'pos_sub_mid': { left: 32, top: 88, role: 'SUB' },
      'ball': { left: 50, top: 50, role: 'BALL' },
      'opp_gk': { left: 95, top: 50, role: 'GK' },
      'opp_p1': { left: 81, top: 26, role: 'LB' },
      'opp_p2': { left: 84, top: 50, role: 'CB' },
      'opp_p3': { left: 81, top: 74, role: 'RB' },
      'opp_p4': { left: 56, top: 26, role: 'LM' },
      'opp_p5': { left: 55, top: 50, role: 'CM' },
      'opp_p6': { left: 56, top: 74, role: 'RM' },
      'opp_p7': { left: 32, top: 50, role: 'ST' }
    },
    '1-2-4-1': {
      name: '1-2-4-1 (Possession)',
      'pos_gk': { left: 6, top: 50, role: 'GK' },
      'pos_p1': { left: 20, top: 34, role: 'LB' },
      'pos_p2': { left: 40, top: 40, role: 'LCM' },
      'pos_p3': { left: 20, top: 66, role: 'RB' },
      'pos_p4': { left: 43, top: 18, role: 'LM' },
      'pos_p5': { left: 40, top: 60, role: 'RCM' },
      'pos_p6': { left: 43, top: 82, role: 'RM' },
      'pos_p7': { left: 75, top: 50, role: 'ST' },
      'pos_sub_def': { left: 12, top: 88, role: 'SUB' },
      'pos_sub_mid': { left: 32, top: 88, role: 'SUB' },
      'ball': { left: 50, top: 50, role: 'BALL' },
      'opp_gk': { left: 95, top: 50, role: 'GK' },
      'opp_p1': { left: 82, top: 26, role: 'LB' },
      'opp_p2': { left: 61, top: 40, role: 'LCM' },
      'opp_p3': { left: 82, top: 74, role: 'RB' },
      'opp_p4': { left: 58, top: 18, role: 'LM' },
      'opp_p5': { left: 61, top: 60, role: 'RCM' },
      'opp_p6': { left: 58, top: 82, role: 'RM' },
      'opp_p7': { left: 30, top: 50, role: 'ST' }
    },
    '1-1-3-3': {
      name: '1-1-3-3 (Attack)',
      'pos_gk': { left: 6, top: 50, role: 'GK' },
      'pos_p1': { left: 19, top: 50, role: 'CB' },
      'pos_p2': { left: 75, top: 24, role: 'LS' },
      'pos_p3': { left: 72, top: 50, role: 'ST' },
      'pos_p4': { left: 42, top: 22, role: 'LM' },
      'pos_p5': { left: 40, top: 50, role: 'CM' },
      'pos_p6': { left: 42, top: 78, role: 'RM' },
      'pos_p7': { left: 75, top: 76, role: 'RS' },
      'pos_sub_def': { left: 12, top: 88, role: 'SUB' },
      'pos_sub_mid': { left: 32, top: 88, role: 'SUB' },
      'ball': { left: 50, top: 50, role: 'BALL' },
      'opp_gk': { left: 95, top: 50, role: 'GK' },
      'opp_p1': { left: 84, top: 50, role: 'CB' },
      'opp_p2': { left: 30, top: 24, role: 'LS' },
      'opp_p3': { left: 33, top: 50, role: 'ST' },
      'opp_p4': { left: 59, top: 22, role: 'LM' },
      'opp_p5': { left: 61, top: 50, role: 'CM' },
      'opp_p6': { left: 59, top: 78, role: 'RM' },
      'opp_p7': { left: 30, top: 76, role: 'RS' }
    }
  };

  function applyFormation"""
content = re.sub(formations_pattern, new_formations, content, flags=re.DOTALL)

# 6. Rewrite applyFormation to update labels dynamically
apply_pattern = r'function applyFormation\(name\) \{.*?\}\n'
new_apply = """let currentFormation = '1-2-3-2';
  function applyFormation(name) {
    const setup = formations[name];
    if (!setup) return;
    currentFormation = name;
    
    document.querySelectorAll('#btnForm1, #btnForm2, #btnForm3, #btnForm4').forEach(btn => btn?.classList.remove('active'));
    if (name === '1-2-3-2') document.getElementById('btnForm1')?.classList.add('active');
    else if (name === '1-3-3-1') document.getElementById('btnForm2')?.classList.add('active');
    else if (name === '1-2-4-1') document.getElementById('btnForm3')?.classList.add('active');
    else if (name === '1-1-3-3') document.getElementById('btnForm4')?.classList.add('active');
    
    for (const [id, config] of Object.entries(setup)) {
      if (id === 'name') continue;
      const el = document.getElementById(id);
      if (el) { 
        el.style.left = `${config.left}%`; 
        el.style.top = `${config.top}%`; 
        
        if (id.startsWith('pos_p') || id.startsWith('opp_p')) {
          const circle = el.querySelector('.token-circle');
          if (circle) circle.innerHTML = config.role;
          el.setAttribute('data-pos', config.role);
          
          if (id.startsWith('pos_p')) {
            const pId = id.replace('pos_', '');
            const labelEl = document.getElementById(`lbl_side_${pId}`);
            if (labelEl) labelEl.innerHTML = config.role;
          }
        }
      }
    }
    showToast(`Applied Formation ${setup.name}`);
  }
"""
content = re.sub(apply_pattern, new_apply, content, flags=re.DOTALL)

# 7. Sidebar labels
sidebar_pattern = r'<span style="font-weight: bold; width: 60px; font-size: 0.8rem; color: #38bdf8;">\${pos\.id\.toUpperCase\(\)}</span>'
sidebar_replace = """<span id="lbl_side_${pos.id}" style="font-weight: bold; width: 60px; font-size: 0.8rem; color: #38bdf8;">${pos.id.toUpperCase()}</span>"""
content = re.sub(sidebar_pattern, sidebar_replace, content, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(content)
