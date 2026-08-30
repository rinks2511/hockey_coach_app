import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace MYRA tokens
old_myra = """        <!-- Position Tokens with Defne as CB -->
        <div class="token myra-gk draggable-token" id="pos_gk" data-pos="GK" style="top: 50%; left: 6%;">
          <div class="token-circle" id="circle_gk" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('gk')">GK</div>
          <select class="player-select-pill" id="select_board_gk" onchange="onPositionChanged('gk', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_lb" data-pos="LB" style="top: 24%; left: 23%;">
          <div class="token-circle" id="circle_lb" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lb')">LB</div>
          <select class="player-select-pill" id="select_board_lb" onchange="onPositionChanged('lb', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_cb" data-pos="CB" style="top: 50%; left: 20%;">
          <div class="token-circle" id="circle_cb" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('cb')">CB</div>
          <select class="player-select-pill" id="select_board_cb" onchange="onPositionChanged('cb', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_rb" data-pos="RB" style="top: 76%; left: 23%;">
          <div class="token-circle" id="circle_rb" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rb')">RB</div>
          <select class="player-select-pill" id="select_board_rb" onchange="onPositionChanged('rb', this.value)"></select>
        </div>

        <div class="token myra-sub-def draggable-token" id="pos_sub_def" data-pos="sub_def" style="top: 88%; left: 12%;">
          <div class="token-circle" id="circle_sub_def" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_def')">SUB<span class="sub-tag">DEF</span></div>
          <select class="player-select-pill" id="select_board_sub_def" onchange="onPositionChanged('sub_def', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_lm" data-pos="LM" style="top: 26%; left: 47%;">
          <div class="token-circle" id="circle_lm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lm')">LM</div>
          <select class="player-select-pill" id="select_board_lm" onchange="onPositionChanged('lm', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_cm" data-pos="CM" style="top: 50%; left: 45%;">
          <div class="token-circle" id="circle_cm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('cm')">CM</div>
          <select class="player-select-pill" id="select_board_cm" onchange="onPositionChanged('cm', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_rm" data-pos="RM" style="top: 74%; left: 47%;">
          <div class="token-circle" id="circle_rm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rm')">RM</div>
          <select class="player-select-pill" id="select_board_rm" onchange="onPositionChanged('rm', this.value)"></select>
        </div>

        <div class="token myra-sub-mid draggable-token" id="pos_sub_mid" data-pos="sub_mid" style="top: 88%; left: 32%;">
          <div class="token-circle" id="circle_sub_mid" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_mid')">SUB<span class="sub-tag">MID</span></div>
          <select class="player-select-pill" id="select_board_sub_mid" onchange="onPositionChanged('sub_mid', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_st" data-pos="ST" style="top: 50%; left: 77%;">
          <div class="token-circle" id="circle_st" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('st')">ST</div>
          <select class="player-select-pill" id="select_board_st" onchange="onPositionChanged('st', this.value)"></select>
        </div>"""

new_myra = """        <!-- Position Tokens with Defne as CB -->
        <div class="token myra-gk draggable-token" id="pos_gk" data-pos="GK" style="top: 50%; left: 6%;">
          <div class="token-circle" id="circle_gk" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('gk')">GK</div>
          <select class="player-select-pill" id="select_board_gk" onchange="onPositionChanged('gk', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_ld" data-pos="LD" style="top: 30%; left: 23%;">
          <div class="token-circle" id="circle_ld" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('ld')">LD</div>
          <select class="player-select-pill" id="select_board_ld" onchange="onPositionChanged('ld', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_rd" data-pos="RD" style="top: 70%; left: 23%;">
          <div class="token-circle" id="circle_rd" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rd')">RD</div>
          <select class="player-select-pill" id="select_board_rd" onchange="onPositionChanged('rd', this.value)"></select>
        </div>

        <div class="token myra-sub-def draggable-token" id="pos_sub_def_att" data-pos="sub_def_att" style="top: 88%; left: 12%;">
          <div class="token-circle" id="circle_sub_def_att" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_def_att')">SUB<span class="sub-tag">D/A</span></div>
          <select class="player-select-pill" id="select_board_sub_def_att" onchange="onPositionChanged('sub_def_att', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_lm" data-pos="LM" style="top: 26%; left: 47%;">
          <div class="token-circle" id="circle_lm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lm')">LM</div>
          <select class="player-select-pill" id="select_board_lm" onchange="onPositionChanged('lm', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_cm" data-pos="CM" style="top: 50%; left: 45%;">
          <div class="token-circle" id="circle_cm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('cm')">CM</div>
          <select class="player-select-pill" id="select_board_cm" onchange="onPositionChanged('cm', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_rm" data-pos="RM" style="top: 74%; left: 47%;">
          <div class="token-circle" id="circle_rm" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rm')">RM</div>
          <select class="player-select-pill" id="select_board_rm" onchange="onPositionChanged('rm', this.value)"></select>
        </div>

        <div class="token myra-sub-mid draggable-token" id="pos_sub_mid" data-pos="sub_mid" style="top: 88%; left: 32%;">
          <div class="token-circle" id="circle_sub_mid" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('sub_mid')">SUB<span class="sub-tag">MID</span></div>
          <select class="player-select-pill" id="select_board_sub_mid" onchange="onPositionChanged('sub_mid', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_lf" data-pos="LF" style="top: 35%; left: 70%;">
          <div class="token-circle" id="circle_lf" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('lf')">LF</div>
          <select class="player-select-pill" id="select_board_lf" onchange="onPositionChanged('lf', this.value)"></select>
        </div>

        <div class="token myra-field draggable-token" id="pos_rf" data-pos="RF" style="top: 65%; left: 70%;">
          <div class="token-circle" id="circle_rf" style="cursor: pointer;" title="Double-click to rename" ondblclick="renamePosition('rf')">RF</div>
          <select class="player-select-pill" id="select_board_rf" onchange="onPositionChanged('rf', this.value)"></select>
        </div>"""

if old_myra in content:
    content = content.replace(old_myra, new_myra)
    print("Replaced MYRA tokens")
else:
    print("WARNING: Could not find old_myra tokens")

with open('index.html', 'w') as f:
    f.write(content)
