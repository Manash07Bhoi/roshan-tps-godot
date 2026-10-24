# Baseline Audit — upstream Godot TPS demo

This audit was recorded **before any project file was modified**. All evidence
files referenced below are in [`docs/evidence/`](evidence/) and
[`docs/screenshots/`](screenshots/).

## 1. Source and revision

| Item | Value |
|---|---|
| Upstream repository | <https://github.com/godotengine/tps-demo> |
| Upstream branch | `master` |
| Upstream commit (baseline) | `a82f15448e9b015440d3bbdf5e10801b260c4e9f` — "Update to Godot 4.7.2 (#224)", 2026-08-31 |
| Commits in upstream history | 213 |
| Project name (upstream) | `Godot Third-Person Shooter Demo` |
| `config/features` | `PackedStringArray("4.7")` |
| Main scene | `res://main/main.tscn` |
| Autoloads | `Settings="*res://menu/settings.gd"` |
| Renderer | Forward+ (default; `rendering_device/driver.windows="d3d12"`) |
| Work branch | `roshan-tps` (upstream history kept intact underneath) |

The upstream `master` is already ported to Godot 4.7.2, so it was used as the
starting point; no older revision was needed.

## 2. Execution environment

| Item | Value |
|---|---|
| OS / arch | Debian GNU/Linux 13 (trixie), x86_64, kernel 6.1 |
| CPU / RAM | 2 vCPU, 1.9 GiB RAM (4 GiB swap file added for testing) |
| GPU | **None.** Rendering via Mesa **lavapipe/llvmpipe** (software Vulkan 1.4 / OpenGL 4.5) under **Xvfb** |
| Android device / emulator | None available |
| Git | 2.47.3 · GitHub CLI: not installed (GitHub REST API used instead) |
| Godot | **4.7.2-stable official**, `4.7.2.stable.official.ed1daf0bf` |

### Godot version selection

* `https://godotengine.org/download/archive/` (checked 2026-10-24) lists
  **4.7.2-stable (18 Aug 2026)** as the newest *stable* release; 4.8 is only at
  `beta1`. The GitHub "latest release" API returned the same tag.
* The project uses GDScript only (no C#), so the standard (non-.NET) build was used.
* Download: `Godot_v4.7.2-stable_linux.x86_64.zip` from the official GitHub release.
  * SHA-512 verified against the official `SHA512-SUMS.txt` → **OK**
    (`9aa00f7a…ed54c65`, see `evidence/godot_version.txt`).
  * Zip integrity test → OK. Binary: `ELF 64-bit LSB executable, x86-64`.
  * `--version` → `4.7.2.stable.official.ed1daf0bf`.

## 3. Inventory

### Scripts and the scenes that use them

| Script | Attached in |
|---|---|
| `main/main.gd` | `main/main.tscn` (root scene manager) |
| `menu/menu.gd` | `menu/menu.tscn` (main menu, online panel, settings, loading UI) |
| `menu/settings.gd` | autoload `Settings` (config file + graphics settings) |
| `level/level.gd`, `level/debug.gd` | `level/level.tscn` (level, spawning, F3 debug label) |
| `player/player.gd`, `player/player_input.gd`, `player/camera_noise_shake_effect.gd` | `player/player.tscn` |
| `player/bullet/bullet.gd` | `player/bullet/bullet.tscn` |
| `enemies/red_robot/red_robot.gd`, `parts/part.gd` | `enemies/red_robot/red_robot.tscn` |
| `enemies/red_robot/laser/impact_effect/blast.gd` | `impact_effect.tscn` |
| `enemies/red_robot/parts/part_disappear_effect/part_disappear.gd` | `part_disappear.tscn` |
| `door/door.gd` | `door/door.tscn` |
| `level/forklift/flying_forklift.gd` | `flying_forklift.tscn` |

15 GDScript files, 1,604 lines. 17 `.tscn` scenes.

### Input actions (project.godot)

`move_left/right/forward/back`, `jump`, `aim`, `shoot`, `view_left/right/up/down`
(gamepad right stick), `quit`, `toggle_fullscreen`, `toggle_debug`, plus overridden
`ui_*` actions. Keyboard, mouse and gamepad bindings are present for gameplay
actions. The automated test confirms that all 14 actions referenced from
scripts exist in the InputMap.

### Player-facing frontend that actually exists

| Screen | Implementation | Branding found |
|---|---|---|
| Boot splash | Engine default (Godot logo) | Godot engine splash |
| Window title | `application/config/name` | "Godot Third-Person Shooter Demo" |
| Main menu | `menu/menu.tscn` → `UI/Main` | Title **image** `menu/tps_demo.png` ("TPS Demo") |
| Online (LAN host/connect) | `UI/Online` | none |
| Settings (graphics) | `UI/Settings` | none |
| Loading | `UI/Loading` | "Loading..." |
| In-game HUD | crosshair `player/crosshair.png` (shown while aiming) | none |
| Debug overlay (F3) | `level/debug.gd` label | none |

**Not present upstream (and therefore not invented):** pause menu, audio
settings, controls screen, health bar, game-over screen, exit confirmation,
credits screen. Escape/Start returns from the level to the main menu.

### Licences

`LICENSE.md`: code MIT (© 2018-2021 Juan Linietsky, Godot Engine contributors);
assets CC BY 3.0 (© 2018 Juan Linietsky, Fernando Miguel Calabró); music CC BY 3.0
(© 2018 Christian Fernando Perucchi); materials derived from GameTextures.com.
`menu/font/OFL.txt`: PT Sans © 2010 ParaType Ltd., SIL OFL 1.1.

### Repository size

Working tree 1.3 GB, `.git` 785 MB. Largest blob in history 71 MB
(`level/level.exr`) — below GitHub's 100 MB hard limit, so the full upstream
history can be pushed without Git LFS.

## 4. Baseline validation results (unmodified upstream, Godot 4.7.2)

### Headless import — `evidence/baseline_import.log`

Exit code 0, 40 s. Errors/warnings:

| Message | Source | Classification |
|---|---|---|
| `Failed loading resource: res://door/model/doorsimple_d.png` | `door.dae` references a texture not in the repo | Asset-level, upstream issue [#217](https://github.com/godotengine/tps-demo/issues/217). Door renders with `door.tres` material. **Retained** (asset change forbidden). |
| `Condition "surfaces.is_empty()" … importer_mesh.cpp` | same `door.dae` import | Asset-level, same root cause. **Retained.** |
| `Animation name "Cannon_Charge" already exists in library` | animation import of a robot model | Asset-level, upstream issue [#218](https://github.com/godotengine/tps-demo/issues/218). **Retained.** |
| `HDR output requested, but it is not supported by this display server` | `window/hdr/request_hdr_output=true` | Environment (Xvfb/headless). Harmless. |
| `Ignoring unsupported header information in HDR: GAMMA/PRIMARIES` | `menu/experiment.hdr` | Harmless importer notice. |

### Automated tests on the unmodified project — `evidence/tests_baseline.log`

`RESULT: 22 passed, 3 failed` — the 3 failures were:

1. **`SSAO setting -1 -> ssao_enabled == false  -> got true`** — real defect (see §5).
2. Window title is not "ROSHAN TPS" (expected: branding not yet applied).
3. Loading text is not branded (expected: branding not yet applied).

All gameplay smoke checks (level load, spawn, floor collision, movement, jump,
camera, aim, shooting, enemy damage/death, quit to menu, re-entry) passed on
the unmodified project.

### Graphical runs (Xvfb + software rendering)

* **Forward+ (Vulkan/lavapipe):** boot splash → main menu → settings all render
  correctly (`screenshots/before_main_menu.png`, `before_settings.png`).
  Pressing PLAY freezes the loading screen at **38 %** permanently
  (`before_loading.png`, `evidence/baseline_runtime.log`). `gdb` showed the main
  thread and a worker thread both blocked in `pthread_cond_wait`, 0 % CPU. A
  verbose run shows the freeze right after loading
  `res://enemies/red_robot/laser/circle.mesh` and two
  `SceneForwardClusteredShaderRD` shader-cache misses
  (`evidence/forward_plus_freeze_verbose_excerpt.log`). Raising
  `threading/worker_pool/max_threads` to 6 (temporary `override.cfg`) did not
  help (`evidence/experiment_threads6.log`). The same freeze happens with the
  Vulkan **Mobile** renderer. Headless mode and the OpenGL **Compatibility**
  renderer load the level fine.
  → Classified as an **engine/driver-level deadlock** in Vulkan shader/pipeline
  compilation during threaded loading on this 2-vCPU software-rendered machine.
  Consistent with upstream Godot issue
  [godotengine/godot#123060](https://github.com/godotengine/godot/issues/123060)
  (shader/pipeline compilation deadlock with few worker threads), but not
  confirmed. It could not be tested on real GPU hardware here.
* **Compatibility (OpenGL/llvmpipe, `--rendering-method gl_compatibility`):** the level
  loads and gameplay renders at ≈1 FPS (`before_gameplay_compat.png`).

## 5. Defects and observations

| # | Finding | Evidence | Classification / action |
|---|---|---|---|
| D1 | **SSAO "Disabled" ignored.** `Settings.apply_graphics_settings()` used `if … if … else`; the trailing `else` re-enabled SSAO after "Disabled" set it to false. | Failing test (`tests_baseline.log`); code inspection vs the correct SSIL block | **Project defect → fixed** (one-word `if`→`elif`). |
| D2 | SSAO Medium/High map to inverted engine quality (Medium → HIGH full-res; High → MEDIUM half-res). | Code inspection | Project defect, **intentionally not changed**: swapping would change the default look and performance of every player (default = Medium). Documented. |
| O1 | `physics/3d/physics_engine="Bullet"` — not a valid Godot 4 value (allowed: `DEFAULT`, `Jolt Physics`, `GodotPhysics3D`, `Dummy`). The engine silently falls back to its default 3D physics server. | Probe script output | Leftover from Godot 3. **Not changed**: picking an engine explicitly could change gameplay physics; the game already runs on the default server and all physics tests pass. |
| O2 | `display_server/driver.linuxbsd="wayland"` | project.godot | Falls back to X11 automatically when Wayland is unavailable (verified under Xvfb). No change. |
| O3 | Default display mode is exclusive fullscreen (`settings.gd` DEFAULTS). | Code | Upstream design choice. Retained. |
| O4 | `[Physics interpolation] Interpolated Camera3D triggered from outside physics process (possibly benign)` | `baseline_headless_run.log` (9×, during spawn) | Engine warning, explicitly flagged as possibly benign. Retained. |
| O5 | FIXME in `settings.gd`: shadows aren't re-enabled in the menu after being disabled until restart. | Upstream comment | Known upstream limitation. Retained. |
| O6 | Escape does not close the "Play Online" panel (only the Back button does). | Graphical test | Upstream UX behaviour; not a crash. Retained (no functional changes beyond verified defects). |
| E1 | Forward+/Mobile threaded-load freeze on lavapipe | §4 | Engine/driver-level; environment-specific. Documented as BLOCKED for Forward+ graphical gameplay testing. |
| A1–A3 | `door.dae` missing texture / empty mesh, duplicate `Cannon_Charge` animation | import log | Asset-level, upstream issues #217/#218. Retained (asset modification forbidden). |

No GDScript parse errors, broken `ext_resource` paths, invalid signal
connections or missing input actions were found: all 114 scenes, scripts and
text resources load, and all script-referenced input actions exist.

## 6. Open upstream issues reviewed (2026-10-24)

#218 duplicate `Cannon_Charge` (reproduced) · #217 door.dae → glTF (related to
the missing texture, reproduced) · #192 stutter on first enemy kill (not
measurable on a software renderer) · #190 Linux build errors (old) · #183/#198
mobile settings / perf testing PRs (not merged; not applied) · #176 motion
computation question · #146 GI/character visibility (3.x era) · #129 robots
missing at long range (gameplay design). No fixes were applied blindly from
old issues.
