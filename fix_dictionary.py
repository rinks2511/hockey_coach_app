import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Fix positionDictionary
old_dict = """  const positionDictionary = {
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
  };"""

new_dict = """  const positionDictionary = {
    gk: { en: { code: 'GK', label: 'GK (Goalkeeper)', circle: 'GK' }, nl: { code: 'K', label: 'K (Keeper)', circle: 'K' } },
    ld: { en: { code: 'LD', label: 'LD (Left Defender)', circle: 'LD' }, nl: { code: 'LA', label: 'LA (Linksachter)', circle: 'LA' } },
    rd: { en: { code: 'RD', label: 'RD (Right Defender)', circle: 'RD' }, nl: { code: 'RA', label: 'RA (Rechtsachter)', circle: 'RA' } },
    sub_def_att: { en: { code: 'SUB-D/A', label: 'SUB-D/A (Def/Att Sub)', circle: 'SUB<span class="sub-tag">D/A</span>' }, nl: { code: 'WISSEL-D/A', label: 'WISSEL-D/A', circle: 'WIS<span class="sub-tag">D/A</span>' } },
    lm: { en: { code: 'LM', label: 'LM (Left Midfield)', circle: 'LM' }, nl: { code: 'LM', label: 'LM (Linksmidden)', circle: 'LM' } },
    cm: { en: { code: 'CM', label: 'CM (Center Midfield)', circle: 'CM' }, nl: { code: 'CM', label: 'CM (Centraalmidden)', circle: 'CM' } },
    rm: { en: { code: 'RM', label: 'RM (Right Midfield)', circle: 'RM' }, nl: { code: 'RM', label: 'RM (Rechtsmidden)', circle: 'RM' } },
    sub_mid: { en: { code: 'SUB-MID', label: 'SUB-MID (Midfield Sub)', circle: 'SUB<span class="sub-tag">MID</span>' }, nl: { code: 'WISSEL-MID', label: 'WISSEL-MID', circle: 'WIS<span class="sub-tag">MID</span>' } },
    lf: { en: { code: 'LF', label: 'LF (Left Forward)', circle: 'LF' }, nl: { code: 'LA', label: 'LA (Linksaanvaller)', circle: 'LA' } },
    rf: { en: { code: 'RF', label: 'RF (Right Forward)', circle: 'RF' }, nl: { code: 'RA', label: 'RA (Rechtsaanvaller)', circle: 'RA' } }
  };"""

if old_dict in content:
    content = content.replace(old_dict, new_dict)
    print("Replaced positionDictionary")
else:
    print("WARNING: Could not find old_dict")

# 2. Fix renderPositionLabels
old_labels = """        if (pos.id === 'sub_def') {
          circleEl.innerHTML = `${dict.code.substring(0, 3)}<span class="sub-tag">DEF</span>`;
        } else if (pos.id === 'sub_mid') {"""

new_labels = """        if (pos.id === 'sub_def_att') {
          circleEl.innerHTML = `${dict.code.substring(0, 3)}<span class="sub-tag">D/A</span>`;
        } else if (pos.id === 'sub_mid') {"""

if old_labels in content:
    content = content.replace(old_labels, new_labels)
    print("Replaced renderPositionLabels")
else:
    print("WARNING: Could not find old_labels")

with open('index.html', 'w') as f:
    f.write(content)

