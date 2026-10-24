# Final handoff: ROSHAN TPS

Personal, non-commercial derivative of the official Godot Third-Person Shooter demo.
Developer and modifier: **Roshan**. Every status below is backed by evidence in this
repository. Anything not executed is marked **NOT TESTED**.

## 1. Engine version used

**Godot 4.7.2-stable**, the official standard (non-.NET) Linux x86_64 binary
(`4.7.2.stable.official.ed1daf0bf`). On 2026-10-24 it was the newest stable release
listed on godotengine.org (4.8 was still at beta1). Its SHA-512 was verified against the
official `SHA512-SUMS.txt`, locally and in CI. The engine was not compiled from source.

## 2. Upstream source

<https://github.com/godotengine/tps-demo>, branch `master`, commit
`a82f15448e9b015440d3bbdf5e10801b260c4e9f` ("Update to Godot 4.7.2 (#224)").
The upstream history is preserved; branch `upstream-master` points at that commit.
Nothing was pushed to the upstream repository, and the local `upstream` remote has its
push URL disabled.

## 3. Published repository

* URL: <https://github.com/Manash07Bhoi/roshan-tps-godot>
* Visibility: **Public**, verified through the unauthenticated GitHub API and page.
* Default branch: `main`. The feature branch is `roshan-tps`, kept identical to `main`.

## 4. Commits (feature branch, on top of `a82f154`)

| Commit | Message |
|---|---|
| `8e933e5` | tests: add headless automated test suite |
| `cf678c6` | fix(settings): honour 'Disabled' choice for SSAO |
| `b75e3f0` | branding: text-only ROSHAN TPS rebrand of player-facing strings |
| `feebc70` | tests: add Godot uid file and reword assertion names |
| `5f3fdbc` | ci: add headless import + automated test workflow |
| `bff96c0` | docs: README, third-party notices, attribution, baseline audit, change log |
| `726808b` | media: add 29 s development-story video cut from real captures |
| `21543d8` | docs: add test report and clean-clone validation evidence |
| `6d80148` | ci: allow manual dispatch of the headless import/test workflow |
| *(tip)* | docs: add final handoff and CI evidence (this file) |

A file cannot contain its own commit hash. To get the current tip, run
`git ls-remote https://github.com/Manash07Bhoi/roshan-tps-godot.git main`.
The last commit with game-relevant content that passed CI is **`6d80148`**.

## 5. Push verification

* `6d80148` was pushed; `git ls-remote origin` then showed `refs/heads/main` and
  `refs/heads/roshan-tps` at `6d801485b717e5df0ccd3a2431da809a38e63e75`, matching the
  local `HEAD`.
* Earlier, after the first push of `bff96c0`, files were fetched from
  `raw.githubusercontent.com` at that commit without authentication. README, LICENSE,
  notices, docs, tests, the CI workflow, `project.godot` and `menu/tps_demo.png` all
  returned HTTP 200. The remote `LICENSE.md` is byte-identical to upstream.
* `.git/config` stores no credentials, and the access token never appears in any commit,
  file, log, screenshot or video. This was checked by grep before every push.

## 6. Defects found and repaired

| ID | Problem | Change | Validation |
|---|---|---|---|
| D1 | Choosing **SSAO "Disabled"** in Settings left SSAO on: a trailing `else` re-enabled it. | `menu/settings.gd`: one `if` changed to `elif`, matching the correct SSIL block. | Automated checks failed on upstream and pass after the fix (`docs/evidence/tests_baseline.log` → `tests_after_ssao_fix.log`). |

The full problem / evidence / root cause / change / validation / limitation write-up is in
`docs/CHANGES_FROM_UPSTREAM.md`. The audit is in `docs/BASELINE_AUDIT.md`.

## 7. Verified issues intentionally not changed

| Issue | Why it was left |
|---|---|
| D2: SSAO Medium and High map to swapped engine quality levels | Swapping them would change the default look and performance for every player. |
| O1: `physics_engine="Bullet"` (a Godot 3 leftover, ignored) | Picking a physics engine could change how gameplay feels. All physics tests pass on the default engine. |
| O6: Escape does not close the Online panel | Upstream UX behaviour; there was no mandate for functional changes. |
| A1–A3: upstream asset import errors (`door.dae`, duplicate `Cannon_Charge` animation) | Asset changes were forbidden. Tracked upstream as #217 and #218. |
| E1: Forward+/Mobile level load freezes at 38 % on the GPU-less test VM | Engine/driver-level; it also happens on unmodified upstream. Consistent with godot#123060, not confirmed. |

## 8. Branding (text only)

| Item | Before | After |
|---|---|---|
| `application/config/name` (window title, user-data folder) | Godot Third-Person Shooter Demo | **ROSHAN TPS** |
| `application/config/description` | Godot Third Person Shooter with high quality assets and lighting | ROSHAN TPS - a personal third-person shooter by Roshan, modified from the official Godot TPS demo |
| Loading-screen label (`menu/menu.tscn`) | Loading... | Loading ROSHAN TPS... |
| F3 debug overlay (`level/debug.gd`) | FPS: … | ROSHAN TPS, then FPS: … |

The "TPS Demo" title image, `icon.png`, the boot splash and every other asset are
unchanged. The original branding was **not** removed.

## 9. Asset integrity

526 of the 531 upstream files are byte-identical. The 5 modified files are all text
(README, `project.godot`, `menu/menu.tscn`, `menu/settings.gd`, `level/debug.gd`).
There are 0 deletions or renames, and 0 changed files with asset extensions. Details are in
`docs/TEST_REPORT.md` §5.

## 10. Automated tests

`tests/test_runner.tscn` runs 25 headless checks covering resources, the input map, settings,
the SSAO/SSIL regression, branding, and gameplay smoke tests (load, spawn, collision, move,
jump, camera, aim, shoot, enemy damage and death, quit to menu, re-entry).
The result progression was **22/3 → 23/2 → 25/0** (upstream → SSAO fix → branding).

## 11. CI (GitHub Actions)

* Workflow `godot_ci.yml` runs the headless import and the test suite on ubuntu-24.04 with
  the SHA-512-verified Godot 4.7.2.
* Run **40063929734** on `6d80148` (trigger: `workflow_dispatch`): **success** in 53 s.
  Godot zip `OK`; import showed only the 3 known upstream asset messages; `RESULT: 25 passed,
  0 failed`. Log: `docs/evidence/ci_run_40063929734.log`. Page:
  <https://github.com/Manash07Bhoi/roshan-tps-godot/actions/runs/40063929734>
* **Observed limitation:** pushes to this new repository did not start any workflow runs,
  neither the initial 3-branch push nor the later 1-commit push, even though Actions is
  enabled and both workflows are active. Manual dispatch works, which is why
  `workflow_dispatch` was added. The upstream `static_checks.yml` has no dispatch trigger,
  so it has not run on GitHub. Its script, `file_format.sh`, passed locally before every
  commit.

## 12. Clean clone

A fresh clone of the public repository at `bff96c0` imported in 38.5 s (exit 0) and passed
25/25 tests, with 0 dirty files before and after (`docs/evidence/clean_clone*.log`).
CI then re-validated the newer `6d80148` from a fresh checkout on GitHub's runner.

## 13. Graphical testing

* **PASS, Forward+:** menu, settings, online panel, branded loading text.
* **PASS, Compatibility renderer:** level load, move, camera, aim, shoot, F3 overlay,
  Escape back to the menu, QUIT.
* **BLOCKED, Forward+ and Mobile:** gameplay (see item 7, E1).
* **INCONCLUSIVE, graphical:** jump. It passes in the automated tests.

All runs were software-rendered on a CPU-only VM, so this says nothing about real-GPU
performance or visuals.

## 14. Not tested

* online host/connect between two instances
* gamepad
* audio output
* real GPU and Forward+ visual quality
* Windows and macOS
* Android

## 15. Android

**Not attempted, and not claimed.** The VM had no Android SDK, device, emulator or export
templates, and the upstream project has no touch controls or Android export preset. To try
it yourself:
1. Install the Godot 4.7.2 export templates and the Android SDK/JDK as described in Godot's
   *Exporting for Android* docs.
2. Add an Android export preset with your own debug keystore. Keystores are deliberately
   not committed.
3. Export, then install with `adb install`.

Expect to need on-screen controls (none exist upstream) and the Mobile or Compatibility
renderer.

## 16. Development-story video

[`media/ROSHAN_TPS_Development_Story.mp4`](../media/ROSHAN_TPS_Development_Story.mp4):
29.0 s, 1080×1920, 30 fps, H.264 High with AAC, 6.9 MB.
* Built **only from real footage**: the terminal session, Forward+ menu capture,
  Compatibility gameplay capture and GitHub screenshots.
* Speed-ups (8× and 10×) are labelled on screen. Captions disclose the software rendering,
  and the original logo is visible.
* The music is the game's own track (Perucchi, CC BY 3.0) and is credited.
* Source clips, checksums, build script and editing notes are in `media/`.

## 17. Licences and attribution

* Code: MIT, © 2018-2021 Juan Linietsky and Godot Engine contributors.
* 3D assets and art: CC BY 3.0, © 2018 Juan Linietsky and Fernando Miguel Calabró
  (source materials from GameTextures.com).
* Music: CC BY 3.0, © 2018 Christian Fernando Perucchi.
* Font: PT Sans, © 2010 ParaType, SIL OFL 1.1.
* Engine: Godot, MIT.

`LICENSE.md` is unchanged. The full notices are in `THIRD_PARTY_NOTICES.md` and
`docs/ATTRIBUTION.md`. No upstream authorship is claimed, and the project is not affiliated
with or endorsed by the Godot Foundation or the original authors.
