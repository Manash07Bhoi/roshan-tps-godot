#!/bin/bash
# Real commands, executed live for the screen recording. Only the typing animation is cosmetic.
cd /home/user/tps-demo
godot() { /home/user/tools/Godot_v4.7.2-stable_linux.x86_64 "$@"; }
P=$'\e[1;36mroshan@dev\e[0m:\e[1;34m~/roshan-tps-godot\e[0m$ '
type_cmd() { printf '%s' "$P"; local s="$1"; for ((i=0;i<${#s};i++)); do printf '%s' "${s:$i:1}"; sleep 0.03; done; echo; sleep 0.4; }
clear
type_cmd "git log --oneline -7"
git -c color.ui=always log --oneline -7 | cut -c1-80 | cat; sleep 3
type_cmd "git diff --stat a82f154 -- project.godot menu level"
git -c color.ui=always diff --stat=60 a82f154 -- project.godot menu level | cat; sleep 2
type_cmd "git diff -U0 a82f154 -- menu/settings.gd menu/menu.tscn level/debug.gd project.godot | grep '^[-+][^-+]'"
git -c color.ui=always diff -U0 a82f154 -- menu/settings.gd menu/menu.tscn level/debug.gd project.godot | grep -E $'^(\e\\[[0-9;]*m)?[-+][^-+]' | cat; sleep 6
clear
type_cmd "godot --version"
godot --version; sleep 1
type_cmd "godot --headless --path . res://tests/test_runner.tscn | grep -E 'PASS|FAIL|RESULT'"
godot --headless --path . res://tests/test_runner.tscn 2>&1 | grep -E "PASS|FAIL|RESULT" | sed -e $'s/\\[PASS\\]/\e[1;32m[PASS]\e[0m/' -e $'s/RESULT/\e[1;33mRESULT\e[0m/'; sleep 3
clear
type_cmd "git rev-parse HEAD"
git rev-parse HEAD; sleep 1
type_cmd "git ls-remote https://github.com/Manash07Bhoi/roshan-tps-godot.git main"
git ls-remote https://github.com/Manash07Bhoi/roshan-tps-godot.git main; sleep 4
