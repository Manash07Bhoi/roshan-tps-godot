# Editing notes: `ROSHAN_TPS_Development_Story.mp4`

| Property | Value (measured with `ffprobe`) |
|---|---|
| Duration | 29.0 s |
| Resolution / aspect | 1080 × 1920, 9:16 vertical |
| Frame rate | 30 fps (constant) |
| Video | H.264 High profile, yuv420p, `+faststart` |
| Audio | AAC-LC 48 kHz stereo, 160 kb/s, loudness-normalised to about −16 LUFS |
| File size | 7.4 MB |
| SHA-256 | `1f6578971157aadc0326601061c62f22626f102176871ad1dfc94530f2520db1` |

## Honesty rules followed

* **Only real footage.** Every pixel of game, terminal or GitHub content comes from
  a recording or screenshot made during this work. Nothing is AI-generated, mocked
  up or re-staged. The only things added are captions, coloured frames and fades.
* **Speed changes are labelled on screen.** The test-run wait is shown at 8× speed
  and gameplay at 10× speed, each with a "SPEED" badge.
* **The rendering limitation is disclosed on screen.** The gameplay was captured
  with the OpenGL Compatibility renderer on a CPU-only cloud VM, at about 1 FPS.
  The default Forward+ renderer cannot load the level on that machine; see
  `docs/TEST_REPORT.md`. The video does **not** show Forward+ gameplay because none
  exists.
* **The original logo is visible.** The "TPS Demo" title image appears in the menu
  shot, because the rebrand is text-only and the original assets were not touched.
  The caption says so: "Original art, logo and assets preserved".
* **No Godot editor footage.** All work was done with the headless Godot binary and
  a terminal, so the video shows the terminal, not an editor UI.
* **Cosmetic terminal prompt.** The terminal prompt reads `roshan@dev:~/roshan-tps-godot`.
  It is cosmetic text printed by `tools/terminal_session.sh`; the real working
  directory was the local clone. Every command shown was really executed live and
  its output is unedited. `godot` is a shell function that calls the official
  `Godot_v4.7.2-stable_linux.x86_64` binary.
* **The SHA shown is a snapshot.** `bff96c0` is the commit that was on GitHub when the
  terminal session was recorded. The commit that adds this video and the final
  reports comes after it; see `docs/FINAL_HANDOFF.md` for the final SHA.

## Timeline

Each segment fades into the next over 0.3 s.

| Time (s) | Segment | Real source (in `source_clips/`) | Source range | Edit |
|---|---|---|---|---|
| 0.0–3.4 | 1/6 "ONE DEMO. A PERSONAL VISION." | `upstream_repo_page.png`: Playwright screenshot of github.com/godotengine/tps-demo showing commit a82f154 and 213 commits | still image | 1.5× crop of the header and file list, slow pan |
| 3.1–7.7 | 2/6 "AUDIT. REPAIR. REBRAND." | `terminal_session_real.mp4` | 0.3–2.3 s (`git log`) and 10.3–12.9 s (compact `git diff` vs a82f154) | trim |
| 7.4–11.4 | 3/6 "TESTED ON GODOT 4.7.2" | `terminal_session_real.mp4` | 17.0–29.4 s at **8×**, then 29.4–31.9 s at 1× (25 `[PASS]` lines, `RESULT: 25 passed, 0 failed`) | trim, speed ramp, "8× SPEED" badge |
| 11.1–15.1 | 4/6 "TEXT-ONLY REBRAND" | `menu_forward_plus_real.mp4`: Forward+ renderer, Xvfb capture at 960×540 and 5 fps | 1.0–2.8 s (main menu), 67.0–69.2 s (loading screen) | scaled to 1080 px; magnified inset of the real "Loading ROSHAN TPS..." label |
| 14.8–21.8 | 5/6 "REAL GAMEPLAY" | `gameplay_compat_excerpt_120-156s.mp4` and `gameplay_compat_excerpt_200-234s.mp4` (120–156 s and 200–234 s of the original 338 s capture) | full excerpts at **10×** | 4:5 crop around the character; magnified inset of the real in-game F3 overlay ("ROSHAN TPS", FPS 1.0); "10× SPEED" badge |
| 21.5–26.1 | 6/6 "LIVE ON GITHUB" | `published_repo_page.png`: Playwright screenshot of the public repo, then `terminal_session_real.mp4` | page pan, then 40.6–42.6 s (`git rev-parse HEAD` and `git ls-remote … main`, both `bff96c0a49c7…`) | 1.5× crop with pan from the header to the README; top crop of the terminal |
| 25.8–29.0 | End card | blurred, darkened frame at 150 s of the gameplay capture | still image | title "ROSHAN TPS", "Built with Godot", "Developer: Roshan", licence credits |

## Audio

The soundtrack is `menu/menu_intro_music.ogg` from the game itself (0–29 s, 0.8 s fade-in,
1.5 s fade-out). It is © 2018 Christian Fernando Perucchi, licensed CC BY 3.0, and is
credited on the end card. No other music or stock sounds were used.

## Fonts

Captions use **PT Sans Bold** (`menu/font/PT_Sans-Web-Bold.ttf`, the game's own font, OFL 1.1),
plus Noto Sans Bold and DejaVu Sans Mono Bold from the Debian font packages.

## How the source footage was recorded

* **Terminal:** `xterm` (62×32, DejaVu Sans Mono 20) on an Xvfb display, recorded by
  `ffmpeg -f x11grab` at 1080×1080 and 15 fps. The script is `tools/terminal_session.sh`.
  Only the letter-by-letter typing is animated; every command runs live.
* **Game:** the official Godot 4.7.2 binary running on Xvfb with Mesa software
  rendering (lavapipe for Vulkan, llvmpipe for OpenGL), recorded by `ffmpeg -f x11grab`
  at 5 fps. Inputs were sent with `xdotool`.
* **GitHub pages:** headless Chromium (Playwright) at 1080 px wide, logged out.

## Rebuilding

```bash
# Requires ffmpeg with libx264, libfreetype (drawtext) and xfade.
python3 media/tools/build_video.py
```

`build_video.py` expects the raw captures in `/home/user/video/raw/` (the paths used on the
build machine). Point `RAW` at `media/source_clips/` and adjust the gameplay trim points
(the excerpts start at 0 instead of 120 s and 200 s) to rebuild from the committed clips.
`source_clips/SHA256SUMS.txt` lists checksums of the committed clips.
`ORIGINAL_FULL_CAPTURES_SHA256.txt` records the checksum of the full 338 s gameplay capture,
which is not committed because of its size (31 MB).

## Not possible here

* **Real-GPU footage.** No GPU was available, so there are no high-frame-rate Forward+
  shots with volumetric fog and GI. To add them: run the game on a GPU machine, record
  with OBS at 1080p60, and replace segment 5 with the new footage at 1× speed. Then
  remove the "10× SPEED" badge and the CPU-only caption.
