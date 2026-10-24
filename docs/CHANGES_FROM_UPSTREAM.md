# Changes from Upstream

Baseline: `godotengine/tps-demo` `master` @ `a82f15448e9b015440d3bbdf5e10801b260c4e9f`
("Update to Godot 4.7.2 (#224)"). Target engine: **Godot 4.7.2-stable** (no
engine-compatibility changes were needed; upstream already targets 4.7).

All work is on branch `roshan-tps`. The upstream history is preserved
unchanged beneath it, so `git diff a82f154..roshan-tps` shows every change.

## Project constraint applied

Rebranding is **text-only**. No image, texture, model, material, animation,
audio, logo, icon, SVG, font, shader or import file was deleted, replaced,
renamed, moved or edited. No scene structure (nodes, layout, signals, resource
paths) was changed. This is verified mechanically in `docs/TEST_REPORT.md`
(§ "Asset integrity").

## 1. Defect repair

### SSAO "Disabled" setting was ignored — `menu/settings.gd`

* **Problem:** choosing *Screen-space Ambient Occlusion → Disabled* and pressing
  Apply left SSAO enabled (a performance cost with no way to turn it off).
* **Evidence:** `tests/test_runner.gd` →
  `[FAIL] SSAO setting -1 -> ssao_enabled == false  -> got true` on the unmodified
  project (`docs/evidence/tests_baseline.log`).
* **Root cause:** the block was `if disabled: … / if medium: … / else: …`. For
  "Disabled", the second `if` is false, so the `else` branch runs and sets
  `ssao_enabled = true`. The SSIL block directly below correctly uses `elif`.
* **Change:** the second `if` became `elif` (one word).
* **Validation:** the same test passes after the fix
  (`docs/evidence/tests_after_ssao_fix.log`). All other tests unchanged.
* **Remaining limitation (intentionally not changed):** Medium/High call the
  engine with swapped qualities (Medium → `ENV_SSAO_QUALITY_HIGH`, full-res;
  High → `ENV_SSAO_QUALITY_MEDIUM`, half-res). Fixing that would alter the
  default visual quality and performance (default is Medium). Retained and
  documented.

## 2. Text-only personal rebranding

| File | Before | After |
|---|---|---|
| `project.godot` → `application/config/name` (window title, OS task bar, user-data folder name) | `Godot Third-Person Shooter Demo` | `ROSHAN TPS` |
| `project.godot` → `application/config/description` | `Godot Third Person Shooter with high quality assets and lighting` | `ROSHAN TPS - a personal third-person shooter by Roshan, modified from the official Godot TPS demo` |
| `menu/menu.tscn` → `UI/Loading/Label` `text` property | `Loading...` | `Loading ROSHAN TPS...` |
| `level/debug.gd` → F3 overlay text | first line `FPS: …` | heading line `ROSHAN TPS` added above `FPS: …` |

**Side effect (documented):** Godot stores user settings in a folder named after
`config/name`. Settings saved under the old name (`…/app_userdata/Godot
Third-Person Shooter Demo/settings.ini`) are not migrated. ROSHAN TPS starts with
default settings the first time.

**Left unchanged on purpose:**

* Main-menu title image `menu/tps_demo.png` ("TPS Demo"), `icon.png` and the
  engine boot splash. These are image assets, and replacing them was explicitly
  forbidden. **The original visual branding is therefore still visible on the
  main menu.**
* Menu button and settings labels (PLAY, PLAY ONLINE, SETTINGS, QUIT, Host,
  Connect, Back, Apply, Cancel, setting names). They contain no demo branding.
* No new screens (credits, pause, controls) were added. They would require new
  scene nodes, which the text-only constraint does not allow.

## 3. Added files (new, no existing file replaced)

| Path | Purpose |
|---|---|
| `tests/test_runner.tscn`, `tests/test_runner.gd`, `tests/test_runner.gd.uid` | Headless automated test suite (25 checks) |
| `.github/workflows/godot_ci.yml` | CI: download Godot 4.7.2 (SHA-512 verified), headless import, run tests |
| `README.md` | Rewritten for ROSHAN TPS (upstream text preserved verbatim in `docs/UPSTREAM_README.md`) |
| `THIRD_PARTY_NOTICES.md` | Licence and credit notices |
| `docs/BASELINE_AUDIT.md`, `docs/ATTRIBUTION.md`, `docs/CHANGES_FROM_UPSTREAM.md`, `docs/TEST_REPORT.md`, `docs/FINAL_HANDOFF.md`, `docs/UPSTREAM_README.md` | Documentation |
| `docs/evidence/*`, `docs/screenshots/*` | Logs and real screenshots from the validation runs |
| `docs/.gdignore`, `media/.gdignore` | Stop Godot from importing documentation images/video as game assets |
| `media/ROSHAN_TPS_Development_Story.mp4` + `media/source_clips/` + `media/EDITING_NOTES.md` | Development-story video and its real source footage |

## 4. Modified files

`README.md` (rewritten), `project.godot` (2 text values), `menu/menu.tscn`
(1 text value), `menu/settings.gd` (1 word), `level/debug.gd` (1 text line).

## 5. Removed files

None.

## 6. Upstream files deliberately kept

`LICENSE.md`, `menu/font/OFL.txt`, `.github/workflows/static_checks.yml`,
`.github/ISSUE_TEMPLATE/*`, `.github/dependabot.yml`, `file_format.sh` and all
assets are untouched.
