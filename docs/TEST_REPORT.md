# Test report: ROSHAN TPS

Date: 2026-10-24 · Engine: **Godot 4.7.2-stable official** (`4.7.2.stable.official.ed1daf0bf`,
SHA-512 verified, see `evidence/godot_version.txt`) · Upstream baseline: `a82f154`.

## Statuses

| Status | Meaning |
|---|---|
| **PASS** | Executed here, and the expected result was observed (evidence linked). |
| **FAIL** | Executed here, and the result was wrong. |
| **BLOCKED** | Attempted, but could not complete for an environmental reason (explained). |
| **NOT TESTED** | Not attempted, because the hardware or setup was unavailable. No claim is made either way. |
| **INCONCLUSIVE** | Attempted, but the observation is not strong enough to call PASS or FAIL. |

## Test environment

Cloud VM: Debian 13 x86_64, 2 vCPU, 1.9 GiB RAM plus 4 GiB swap. **There is no GPU.**
Graphical runs used Xvfb at 1920×1080 with Mesa software rendering (lavapipe for Vulkan,
llvmpipe for OpenGL 4.5). There is no sound device, gamepad, second machine or Android device.
"Headless" means `--headless`, which uses the dummy renderer and dummy audio.

## 1. Summary

| # | Area | Method | Result | Evidence |
|---|---|---|---|---|
| 1 | Engine download integrity | SHA-512 vs official `SHA512-SUMS.txt` | **PASS** | `evidence/godot_version.txt` |
| 2 | Headless import, upstream baseline | `--headless --import` | **PASS** (exit 0; 3 upstream asset errors, see §3) | `evidence/baseline_import.log` |
| 3 | Headless import, modified project | `--headless --import` | **PASS** (exit 0; same 3 upstream asset errors and nothing new) | `evidence/after_import.log` |
| 4 | Automated test suite, final | `res://tests/test_runner.tscn` | **PASS: 25 passed, 0 failed** | `evidence/tests_after_branding.log` |
| 5 | GDScript parse / resource load of all 114 scenes, scripts and resources | test 1 of the suite | **PASS** | same |
| 6 | Main menu, graphical, Forward+ | Xvfb + lavapipe, screenshots | **PASS** | `screenshots/after_main_menu.png` |
| 7 | Settings screen, graphical, Forward+ | open Settings, inspect, Back | **PASS** | `screenshots/after_settings.png` |
| 8 | "Play Online" panel, graphical | open, Back | **PASS** (UI only, no networking) | `screenshots/after_online_panel.png` |
| 9 | Branded loading text, graphical | press PLAY | **PASS**: "Loading ROSHAN TPS..." shown | `screenshots/after_loading.png` |
| 10 | Window title "ROSHAN TPS" | automated test and `project.godot` | **PASS** | test log |
| 11 | Level load and gameplay, graphical, **Forward+** | press PLAY | **BLOCKED**: loading freezes at 38 % (see §4). This happens identically on unmodified upstream. | `evidence/after_runtime_forward_plus.log`, `screenshots/before_loading.png` |
| 12 | Level load and gameplay, graphical, **Mobile** renderer | press PLAY | **BLOCKED**: same 38 % freeze (experiment on upstream) | `evidence/experiment_mobile_renderer.log` |
| 13 | Level load, graphical, **Compatibility** renderer | `--rendering-method gl_compatibility` | **PASS** | `screenshots/after_gameplay_spawn.png` |
| 14 | Move forward, graphical (Compatibility) | hold W | **PASS** | `screenshots/after_gameplay_move_forward.png` |
| 15 | Camera turn, graphical (Compatibility) | mouse motion via xdotool | **PASS** | `screenshots/after_gameplay_camera_turn.png` |
| 16 | Aim, graphical (Compatibility) | hold RMB | **PASS** | `screenshots/after_gameplay_aim.png` |
| 17 | Shoot, graphical (Compatibility) | LMB while aiming | **PASS** | `screenshots/after_gameplay_shoot.png` |
| 18 | Jump, graphical (Compatibility) | Space | **INCONCLUSIVE**: at about 1 FPS the jump was not clearly captured on screen. It is covered by automated checks 17–18 (§2), which pass. | `evidence/after_runtime_compat_gameplay.log` |
| 19 | F3 debug overlay shows "ROSHAN TPS" | F3 in game | **PASS** | `screenshots/after_gameplay_aim.png` (top-left) |
| 20 | Escape returns to the menu; QUIT exits cleanly | graphical (Compatibility) | **PASS** (process exit code 0) | `screenshots/after_back_to_menu.png`, runtime log |
| 21 | SSAO "Disabled" honoured (defect D1) | automated checks 4–9 | **PASS** after the fix (it **FAILED** on upstream) | `evidence/tests_baseline.log` vs `tests_after_ssao_fix.log` |
| 22 | Clean clone from GitHub, then import and tests | fresh `git clone` of the public repo | **PASS** (see §6) | `evidence/clean_clone*.log` |
| 23 | GitHub Actions CI (import and tests on ubuntu-24.04) | workflow `godot_ci.yml` | see §7 | Actions tab |
| 24 | Online multiplayer: host / connect | (none) | **NOT TESTED**: needs two networked game instances with a working renderer; the UI panel was tested only (row 8) | (none) |
| 25 | Gamepad input | (none) | **NOT TESTED**: no controller. Gamepad bindings exist in the input map (automated check 2 confirms the actions exist, not the devices). | (none) |
| 26 | Audio output (music, SFX) | (none) | **NOT TESTED**: no sound device (headless uses dummy audio). The audio files are unchanged from upstream. | (none) |
| 27 | Performance on a real GPU, Forward+ visuals (GI, fog, SSAO, SSIL) | (none) | **NOT TESTED**: no GPU | (none) |
| 28 | Android export / install | (none) | **NOT TESTED**: no Android SDK, device or emulator, no export templates, and no touch controls exist upstream. No APK was produced and none is claimed. | (none) |
| 29 | Windows / macOS | (none) | **NOT TESTED** | (none) |

## 2. Automated tests (`tests/test_runner.gd`)

The suite runs headless and exits with code 0 only if every check passes:

```bash
godot --headless --import --path .
godot --headless --path . res://tests/test_runner.tscn
```

| # | Check | What it proves |
|---|---|---|
| 1 | All 114 scenes, scripts and text resources load | No parse errors or broken `ext_resource` paths |
| 2 | All 14 input actions used by scripts exist in the InputMap | Controls are wired |
| 3 | Settings autoload populates every default key | Settings file and defaults are intact |
| 4–9 | SSAO setting −1/2/3 and SSIL setting −1/2/3 map to `*_enabled` correctly | Regression test for defect D1 |
| 10 | Window/application title is "ROSHAN TPS" | Branding applied |
| 11 | Loading screen text shows "ROSHAN TPS" | Branding applied |
| 12 | Menu → level transition completes | Threaded level loading works (headless) |
| 13 | Local player spawned | Spawn logic |
| 14 | Enemy robots spawned (4) | Enemy placement |
| 15 | Player lands on the floor | Level collision |
| 16 | Forward input moves the player | Movement |
| 17 | Jump input lifts the player | Jump |
| 18 | Player lands again after jumping | Gravity and landing |
| 19 | Mouse motion rotates the camera | Camera input |
| 20 | Aim input enters aiming mode | Aim |
| 21 | Shooting while aiming spawns bullets | Shooting |
| 22 | Enemy takes damage when hit | Damage |
| 23 | Enemy dies and emits `exploded` at zero health | Enemy death |
| 24 | Quit action returns to the main menu | Back to menu |
| 25 | A second session starts after returning to the menu | Scene re-entry (no stale state) |

(The suite prints 25 `[PASS]` lines; row 4–9 covers 6 individual checks.)

### Progression

Each stage was reproduced in a temporary git worktree with the same test suite:

| Stage | Commit | Result | Failures |
|---|---|---|---|
| Unmodified upstream | `a82f154` + test files | **22 passed, 3 failed** | SSAO −1 → `ssao_enabled` stayed true (real defect D1); title not branded; loading text not branded |
| After the SSAO fix | `cf678c6` | **23 passed, 2 failed** | the two branding checks (branding not yet applied) |
| After the text-only branding | `b75e3f0` onward | **25 passed, 0 failed** | (none) |

The logs are `evidence/tests_baseline.log`, `tests_after_ssao_fix.log` and `tests_after_branding.log`.
The two branding checks were written before the branding change, so they were *expected*
to fail on upstream; they are not upstream defects.

Limitations of the automated tests: they run with the dummy renderer and dummy audio, and they
drive the game through `Input.parse_input_event`. They check game logic, not rendering
quality, frame rate, audio, networking or real devices.

## 3. Import warnings (unchanged from upstream)

| Message | Classification |
|---|---|
| `Failed loading resource: res://door/model/doorsimple_d.png` | Upstream asset (issue #217). Retained, because modifying assets is out of scope. |
| `Condition "surfaces.is_empty()" is true` (door.dae) | Same root cause. Retained. |
| `Animation name "Cannon_Charge" already exists in library` | Upstream asset (issue #218). Retained. |
| `HDR output requested, but it is not supported by this display server` | Headless/Xvfb environment. Harmless. |
| `Ignoring unsupported header information in HDR` | Importer notice. Harmless. |

The baseline, modified and clean-clone imports show exactly the same set.

## 4. BLOCKED: Forward+ / Mobile level load on this machine

* **Symptom:** after PLAY, the loading bar stops at 38 % forever. CPU usage is 0 %, and
  `gdb` shows the main thread and a worker both waiting in `pthread_cond_wait`.
* **Same on unmodified upstream:** yes, so it is not caused by any ROSHAN TPS change.
* **Experiments:** a worker pool of 6 threads still froze; the Mobile renderer also froze; the
  Compatibility renderer and headless mode load fine.
* **Classification:** an engine/driver-level deadlock in Vulkan shader/pipeline compilation
  during threaded loading on a 2-vCPU software (lavapipe) device. It is **consistent with**
  [godotengine/godot#123060](https://github.com/godotengine/godot/issues/123060), but **not
  confirmed**.
* **What this does not mean:** it is no evidence that the game fails on real GPUs. That is
  simply **NOT TESTED** (row 27).

## 5. Asset integrity

The rebrand was required to be text-only, with no asset added, removed, renamed or modified.
This was verified mechanically against upstream `a82f154`, on the final tree including
`docs/` and `media/`:

| Check | Result |
|---|---|
| Files tracked upstream | 531 |
| …still present and **byte-identical** (same blob hash and path) | **526** |
| …modified | **5**, all text: `README.md`, `project.godot` (name and description strings), `menu/menu.tscn` (one Label `text`), `menu/settings.gd` (`if` → `elif`), `level/debug.gd` (overlay text) |
| Deleted / renamed / copied (`git diff -M --name-status`) | **0** |
| Changed files with asset extensions (png, jpg, exr, hdr, svg, dae, glb, mesh, res, tres, material, anim, ogg, wav, ttf, shader, import, …) | **0** |
| `menu/tps_demo.png` (original title logo), `icon.png`, boot splash | unchanged, still used |
| Added files | 58: tests (3), CI workflow (1), docs, evidence, screenshots, `THIRD_PARTY_NOTICES.md`, `media/` |

`docs/` and `media/` contain a `.gdignore`, so Godot never imports the documentation images
or the video as game assets. `LICENSE.md` is byte-identical to upstream.

To reproduce:

```bash
git diff --name-status -M a82f154 HEAD | grep -v '^A'
```

## 6. Clean clone validation

A fresh clone of the **public** GitHub repo was made into an empty directory with no
local state, and validated there. Logs: `evidence/clean_clone.log`, `clean_clone_import.log`,
`clean_clone_tests.log`.

| Step | Result |
|---|---|
| `git clone https://github.com/Manash07Bhoi/roshan-tps-godot.git` | exit 0, 16 s |
| Checked-out commit | `bff96c0a49c76e117e61d8e66fc8b6a00370f703` (`main`) |
| Dirty files right after the clone | 0 |
| `godot --headless --import` (cold, no `.godot/` cache) | exit 0, 38.5 s; only the 3 upstream asset messages from §3 |
| Test suite | exit 0, `RESULT: 25 passed, 0 failed` |
| Dirty files after import and tests | 0 (the import cache is git-ignored) |

The later commit that adds `media/` and these reports does not change any game file. CI
(§7) re-validates every pushed commit.

## 7. Continuous integration

Workflow `.github/workflows/godot_ci.yml` runs on push, pull request and manual dispatch:
1. On ubuntu-24.04, download the official Godot 4.7.2 binary and verify its SHA-512.
2. Run the headless import, failing on `SCRIPT ERROR` or `Parse Error`.
3. Run the test suite, which must print `RESULT: … 0 failed`.
4. Upload the logs as artifacts.

The upstream `static_checks.yml` (`file_format.sh`) is kept. That script also passes
locally on every commit.

CI run results are recorded in `docs/FINAL_HANDOFF.md` (item 11). Upstream's initial
3-branch push to the new repository did not trigger any workflow runs, so the first runs
come from the push that adds this report.

## 8. Graphical-test caveats

* Graphical runs were software-rendered at 960×540 or 1920×1080. The Compatibility renderer
  ran at about 1 FPS, so inputs were held for tens of seconds and screenshots were taken
  after each action.
* Screenshots under `screenshots/` are unedited captures from those runs.
* No claim is made about visual quality, frame rate or feel on real hardware.
