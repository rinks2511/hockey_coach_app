import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace MYRA tokens
old_myra = """        <div class="token myra-gk draggable-token" id="pos_gk" data-pos="GK" style="top: 50%; left: 6%;">
          <div class="token-circle" id="circle_gk" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('gk')">GK</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_lb" data-pos="LB" style="top: 24%; left: 23%;">
          <div class="token-circle" id="circle_lb" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lb')">LB</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_cb" data-pos="CB" style="top: 50%; left: 20%;">
          <div class="token-circle" id="circle_cb" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('cb')">CB</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_rb" data-pos="RB" style="top: 76%; left: 23%;">
          <div class="token-circle" id="circle_rb" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rb')">RB</div>
        </div>
        <div class="token myra-sub-def draggable-token" id="pos_sub_def" data-pos="sub_def" style="top: 88%; left: 12%;">
          <div class="token-circle" id="circle_sub_def" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_def')">SUB<span class="sub-tag">DEF</span></div>
        </div>
        <div class="token myra-field draggable-token" id="pos_lm" data-pos="LM" style="top: 26%; left: 47%;">
          <div class="token-circle" id="circle_lm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lm')">LM</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_cm" data-pos="CM" style="top: 50%; left: 45%;">
          <div class="token-circle" id="circle_cm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('cm')">CM</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_rm" data-pos="RM" style="top: 74%; left: 47%;">
          <div class="token-circle" id="circle_rm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rm')">RM</div>
        </div>
        <div class="token myra-sub-mid draggable-token" id="pos_sub_mid" data-pos="sub_mid" style="top: 88%; left: 32%;">
          <div class="token-circle" id="circle_sub_mid" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_mid')">SUB<span class="sub-tag">MID</span></div>
        </div>
        <div class="token myra-field draggable-token" id="pos_st" data-pos="ST" style="top: 50%; left: 77%;">
          <div class="token-circle" id="circle_st" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('st')">ST</div>
        </div>"""

new_myra = """        <div class="token myra-gk draggable-token" id="pos_gk" data-pos="GK" style="top: 50%; left: 6%;">
          <div class="token-circle" id="circle_gk" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('gk')">GK</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_ld" data-pos="LD" style="top: 30%; left: 23%;">
          <div class="token-circle" id="circle_ld" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('ld')">LD</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_rd" data-pos="RD" style="top: 70%; left: 23%;">
          <div class="token-circle" id="circle_rd" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rd')">RD</div>
        </div>
        <div class="token myra-sub-def draggable-token" id="pos_sub_def_att" data-pos="sub_def_att" style="top: 88%; left: 12%;">
          <div class="token-circle" id="circle_sub_def_att" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_def_att')">SUB<span class="sub-tag">DEF</span></div>
        </div>
        <div class="token myra-field draggable-token" id="pos_lm" data-pos="LM" style="top: 26%; left: 47%;">
          <div class="token-circle" id="circle_lm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lm')">LM</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_cm" data-pos="CM" style="top: 50%; left: 45%;">
          <div class="token-circle" id="circle_cm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('cm')">CM</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_rm" data-pos="RM" style="top: 74%; left: 47%;">
          <div class="token-circle" id="circle_rm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rm')">RM</div>
        </div>
        <div class="token myra-sub-mid draggable-token" id="pos_sub_mid" data-pos="sub_mid" style="top: 88%; left: 32%;">
          <div class="token-circle" id="circle_sub_mid" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_mid')">SUB<span class="sub-tag">MID</span></div>
        </div>
        <div class="token myra-field draggable-token" id="pos_lf" data-pos="LF" style="top: 35%; left: 70%;">
          <div class="token-circle" id="circle_lf" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lf')">LF</div>
        </div>
        <div class="token myra-field draggable-token" id="pos_rf" data-pos="RF" style="top: 65%; left: 70%;">
          <div class="token-circle" id="circle_rf" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rf')">RF</div>
        </div>"""

if old_myra in content:
    content = content.replace(old_myra, new_myra)
    print("Replaced MYRA tokens")
else:
    print("WARNING: Could not find old_myra tokens")

# Replace Opponent tokens
old_opp = """        <div class="token opp draggable-token" id="opp_gk" style="top: 50%; left: 95%;"><div class="token-circle">GK</div></div>
        <div class="token opp draggable-token" id="opp_lb" style="top: 26%; left: 81%;"><div class="token-circle">LB</div></div>
        <div class="token opp draggable-token" id="opp_cb" style="top: 50%; left: 84%;"><div class="token-circle">CB</div></div>
        <div class="token opp draggable-token" id="opp_rb" style="top: 74%; left: 81%;"><div class="token-circle">RB</div></div>
        <div class="token opp draggable-token" id="opp_lm" style="top: 26%; left: 56%;"><div class="token-circle">LM</div></div>
        <div class="token opp draggable-token" id="opp_cm" style="top: 50%; left: 55%;"><div class="token-circle">CM</div></div>
        <div class="token opp draggable-token" id="opp_rm" style="top: 74%; left: 56%;"><div class="token-circle">RM</div></div>
        <div class="token opp draggable-token" id="opp_st" style="top: 50%; left: 32%;"><div class="token-circle">ST</div></div>"""

new_opp = """        <div class="token opp draggable-token" id="opp_gk" style="top: 50%; left: 95%;"><div class="token-circle">GK</div></div>
        <div class="token opp draggable-token" id="opp_ld" style="top: 30%; left: 81%;"><div class="token-circle">LD</div></div>
        <div class="token opp draggable-token" id="opp_rd" style="top: 70%; left: 81%;"><div class="token-circle">RD</div></div>
        <div class="token opp draggable-token" id="opp_lm" style="top: 26%; left: 56%;"><div class="token-circle">LM</div></div>
        <div class="token opp draggable-token" id="opp_cm" style="top: 50%; left: 55%;"><div class="token-circle">CM</div></div>
        <div class="token opp draggable-token" id="opp_rm" style="top: 74%; left: 56%;"><div class="token-circle">RM</div></div>
        <div class="token opp draggable-token" id="opp_lf" style="top: 35%; left: 32%;"><div class="token-circle">LF</div></div>
        <div class="token opp draggable-token" id="opp_rf" style="top: 65%; left: 32%;"><div class="token-circle">RF</div></div>"""

if old_opp in content:
    content = content.replace(old_opp, new_opp)
    print("Replaced OPP tokens")
else:
    print("WARNING: Could not find old_opp tokens")

with open('index.html', 'w') as f:
    f.write(content)
