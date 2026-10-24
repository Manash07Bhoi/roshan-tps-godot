#!/usr/bin/env python3
"""Build ROSHAN_TPS_Development_Story.mp4 (1080x1920, 30 fps, H.264) from REAL captures only.

Every visual comes from a real recording or real screenshot in video/raw/:
  clip_terminal_session.mp4   real xterm session (git log, git diff, godot --version, tests, rev-parse, ls-remote)
  clip_menu_forward_plus.mp4  real Xvfb capture, Forward+ renderer (menu + branded loading screen)
  clip_gameplay_compat.mp4    real Xvfb capture, Compatibility renderer gameplay (~1 FPS, software GPU)
  upstream_repo_page.png      real Playwright screenshot of github.com/godotengine/tps-demo
  published_repo_page.png     real Playwright screenshot of github.com/Manash07Bhoi/roshan-tps-godot
Only editing operations are applied: trim, speed change (labelled on screen), crop/scale,
magnified insets of real pixels, captions, fades. Music: the game's own menu_intro_music.ogg
(Christian Fernando Perucchi, CC BY 3.0, credited on the end card).
"""
import os, subprocess, json

ROOT = "/home/user"
RAW = f"{ROOT}/video/raw"
WORK = "/var/tmp/roshan_video"          # large intermediates stay outside the repo
TXT = f"{WORK}/txt"
GAME = f"{ROOT}/tps-demo"
OUT = f"{GAME}/media/ROSHAN_TPS_Development_Story.mp4"
os.makedirs(TXT, exist_ok=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)

FONT_B = f"{GAME}/menu/font/PT_Sans-Web-Bold.ttf"      # the game's own font (OFL 1.1)
FONT_N = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_M = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
BG = "0x0d1117"
ACCENT = "0xff9b50"
GREY = "0x8b949e"
FPS = 30
XF = 0.3   # crossfade length

_n = 0
def tfile(text):
    """drawtext reads from textfile= so no escaping issues."""
    global _n
    _n += 1
    p = f"{TXT}/t{_n:03d}.txt"
    with open(p, "w") as f:
        f.write(text)
    return p

def dt(text, y, size, color="white", font=FONT_B, x="(w-text_w)/2", start=0.0, end=None, fade=0.3, box=False):
    en = f":enable='between(t,{start},{end})'" if end is not None else (f":enable='gte(t,{start})'" if start else "")
    alpha = f"if(lt(t,{start}),0,min(1,(t-{start})/{fade}))"
    b = ":box=1:boxcolor=0x000000@0.65:boxborderw=14" if box else ""
    return (f"drawtext=fontfile={font}:textfile={tfile(text)}:fontsize={size}:fontcolor={color}"
            f":x={x}:y={y}:alpha='{alpha}'{b}{en}")

def chrome(idx, head1, head2, sub, footer):
    """Common caption layout inside the vertical safe zone."""
    f = [dt(f"ROSHAN TPS  ·  DEV STORY  ·  {idx}/6", 120, 30, GREY, start=0)]
    f.append(dt(head1, 190, 92, "white", start=0.05))
    yy = 290
    if head2:
        f.append(dt(head2, 290, 92, "white", start=0.15)); yy = 390
    f.append(f"drawbox=x=440:y={yy+8}:w=200:h=6:color={ACCENT}:t=fill")
    f.append(dt(sub, yy + 34, 40, ACCENT, start=0.25))
    f.append(dt(footer, 1640, 30, GREY, start=0.3))
    return f

def run(cmd):
    print(" ".join(cmd)[:300], flush=True)
    subprocess.run(cmd, check=True)

ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]

def seg(name, dur, inputs, fc):
    out = f"{WORK}/{name}.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y"]
    for i in inputs:
        cmd += i
    cmd += ["-f", "lavfi", "-t", str(dur), "-i", f"color=c={BG}:s=1080x1920:r={FPS}"]
    cmd += ["-filter_complex", fc, "-map", "[v]", "-t", str(dur)] + ENC + [out]
    run(cmd)
    return out, dur

segments = []

# ---- S1: upstream repository (real Playwright screenshot) -------------------------------
D = 3.4
c = chrome(1, "ONE DEMO.", "A PERSONAL VISION.", "Starting point: the official Godot TPS demo",
           "github.com/godotengine/tps-demo  ·  upstream commit a82f154")
fc = (f"[0:v]crop=720:747:0:'40+90*t/{D}',scale=1080:1120:flags=lanczos,setsar=1[img];"
      f"[1:v][img]overlay=0:500:shortest=1,drawbox=x=0:y=496:w=1080:h=4:color={ACCENT}:t=fill," + ",".join(c) + "[v]")
segments.append(seg("s1", D, [["-loop", "1", "-framerate", str(FPS), "-t", str(D), "-i", f"{RAW}/upstream_repo_page.png"]], fc))

# ---- S2: audit / repair / rebrand (real terminal: git log + compact real diff) ----------
D = 4.6
c = chrome(2, "AUDIT. REPAIR.", "REBRAND.", "1 verified bug fix  ·  text-only branding",
           "Real terminal session  ·  git diff vs upstream a82f154")
fc = (f"[0:v]trim=0.3:2.3,setpts=PTS-STARTPTS[a];[0:v]trim=10.3:12.9,setpts=PTS-STARTPTS[b];"
      f"[a][b]concat=n=2:v=1,fps={FPS},setsar=1[term];"
      f"[1:v][term]overlay=0:520:shortest=1,drawbox=x=0:y=516:w=1080:h=4:color={ACCENT}:t=fill," + ",".join(c) + "[v]")
segments.append(seg("s2", D, [["-i", f"{RAW}/clip_terminal_session.mp4"]], fc))

# ---- S3: tests (real terminal: test run sped up 8x while waiting, then results at 1x) ---
D = 4.0
c = chrome(3, "TESTED ON", "GODOT 4.7.2", "25 automated checks  ·  25 passed  ·  0 failed",
           "Headless test run  ·  waiting part shown at 8× speed")
fc = (f"[0:v]trim=17:29.4,setpts=(PTS-STARTPTS)/8[a];[0:v]trim=29.4:31.9,setpts=PTS-STARTPTS[b];"
      f"[a][b]concat=n=2:v=1,fps={FPS},setsar=1[term];"
      f"[1:v][term]overlay=0:520:shortest=1,drawbox=x=0:y=516:w=1080:h=4:color={ACCENT}:t=fill,"
      + ",".join(c) + "," + dt("8× SPEED", 560, 34, "black", font=FONT_N, x="w-text_w-40", start=0, end=1.5) .replace("fontcolor=black", "fontcolor=black:box=1:boxcolor=" + ACCENT + ":boxborderw=10")
      + "[v]")
segments.append(seg("s3", D, [["-i", f"{RAW}/clip_terminal_session.mp4"]], fc))

# ---- S4: branded interface (real Forward+ capture: menu, then branded loading text) -----
D = 4.0
c = chrome(4, "TEXT-ONLY", "REBRAND", "Original art, logo and assets preserved",
           "Real capture  ·  Forward+ renderer  ·  menu + loading screen")
fc = (f"[0:v]trim=1.0:2.8,setpts=PTS-STARTPTS[a];[0:v]trim=67:69.2,setpts=PTS-STARTPTS[b];"
      f"[a][b]concat=n=2:v=1,fps={FPS},scale=1080:608:flags=lanczos,setsar=1,split[g][g2];"
      f"[g2]crop=360:46:30:518,scale=1080:138:flags=lanczos,trim=1.8:{D},setpts=PTS-STARTPTS+1.8/TB[zoom];"
      f"[1:v][g]overlay=0:560:shortest=1,drawbox=x=0:y=556:w=1080:h=4:color={ACCENT}:t=fill[base];"
      f"[base][zoom]overlay=0:1250:enable='gte(t,1.8)',"
      f"drawbox=x=0:y=1246:w=1080:h=144:color={ACCENT}:t=4:enable='gte(t,1.8)',"
      + ",".join(c) + "," + dt("MAGNIFIED: real loading-screen text", 1410, 30, "white", start=1.9) + "[v]")
segments.append(seg("s4", D, [["-i", f"{RAW}/clip_menu_forward_plus.mp4"]], fc))

# ---- S5: real gameplay (Compatibility renderer, 10x speed, labelled) --------------------
D = 7.0
c = chrome(5, "REAL", "GAMEPLAY", "Move  ·  look  ·  aim  ·  shoot",
           "Compatibility renderer on a CPU-only VM (≈1 FPS)  ·  10× speed")
fc = (f"[0:v]split[s1][s2];"
      f"[s1]trim=120:156,setpts=(PTS-STARTPTS)/10,crop=432:540:264:0[a];"
      f"[s2]trim=200:234,setpts=(PTS-STARTPTS)/10,crop=432:540:40:0[b];"
      f"[a][b]concat=n=2:v=1,fps={FPS},scale=1000:1250:flags=lanczos,setsar=1[gp];"
      f"[0:v]trim=120:156,setpts=(PTS-STARTPTS)/10,crop=150:66:0:0[o1];"
      f"[0:v]trim=200:234,setpts=(PTS-STARTPTS)/10,crop=150:66:0:0[o2];"
      f"[o1][o2]concat=n=2:v=1,fps={FPS},scale=450:198:flags=lanczos,setsar=1[ov];"
      f"[1:v][gp]overlay=40:520:shortest=1,drawbox=x=36:y=516:w=1008:h=1258:color={ACCENT}:t=4[base];"
      f"[base][ov]overlay=60:540,drawbox=x=58:y=538:w=454:h=202:color=white@0.85:t=3,"
      + ",".join(c[:-1]) + "," + dt("10× SPEED", 1690, 34, "black", font=FONT_N, x="w-text_w-60", start=0)
        .replace("fontcolor=black", "fontcolor=black:box=1:boxcolor=" + ACCENT + ":boxborderw=10")
      + "," + dt("Compatibility renderer · CPU-only VM (≈1 FPS)", 1800, 30, GREY, start=0.3)
      + "," + dt("In-game F3 overlay (magnified)", 762, 26, "white", x="60", start=0.3, box=True) + "[v]")
segments.append(seg("s5", D, [["-i", f"{RAW}/clip_gameplay_compat.mp4"]], fc))

# ---- S6: published repo (real screenshot pan) + real ls-remote SHA match ------------------
D = 4.6
c = chrome(6, "LIVE ON", "GITHUB", "Public repo  ·  pushed SHA verified",
           "github.com/Manash07Bhoi/roshan-tps-godot")
fc = (f"[0:v]crop=720:747:0:'min(853,40+813*t/2.3)',scale=1080:1120:flags=lanczos,setsar=1,trim=0:2.6,setpts=PTS-STARTPTS[pg];"
      f"[2:v]trim=40.6:42.6,setpts=PTS-STARTPTS,crop=1080:200:0:0,fps={FPS},setsar=1,"
      f"setpts=PTS+2.6/TB[sha];"
      f"[1:v][pg]overlay=0:500:eof_action=pass,drawbox=x=0:y=496:w=1080:h=4:color={ACCENT}:t=fill[b1];"
      f"[b1]drawbox=x=0:y=500:w=1080:h=1120:color={BG}:t=fill:enable='gte(t,2.6)'[b2];"
      f"[b2][sha]overlay=0:800:enable='gte(t,2.6)',"
      f"drawbox=x=0:y=796:w=1080:h=208:color={ACCENT}:t=4:enable='gte(t,2.6)',"
      + ",".join(c) + ","
      + dt("local HEAD  =  remote main", 1060, 46, "white", start=2.7)
      + "," + dt("bff96c0a49c7…", 1130, 54, ACCENT, font=FONT_M, start=2.8) + "[v]")
# S6 has two media inputs, so it is built manually (0=page, 1=terminal, 2=background)
out = f"{WORK}/s6.mp4"
fc6 = fc.replace("[1:v][pg]", "[2:v][pg]").replace("[2:v]trim", "[1:v]trim")
run(["ffmpeg", "-loglevel", "error", "-y",
     "-loop", "1", "-framerate", str(FPS), "-t", str(D), "-i", f"{RAW}/published_repo_page.png",
     "-i", f"{RAW}/clip_terminal_session.mp4",
     "-f", "lavfi", "-t", str(D), "-i", f"color=c={BG}:s=1080x1920:r={FPS}",
     "-filter_complex", fc6, "-map", "[v]", "-t", str(D)] + ENC + [out])
segments.append((out, D))

# ---- S7: end card over a blurred real gameplay frame ------------------------------------
D = 3.2
still = f"{WORK}/endcard_frame.png"
run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "150", "-i", f"{RAW}/clip_gameplay_compat.mp4", "-frames:v", "1", still])
fc = (f"[0:v]crop=304:540:328:0,scale=1080:1920:flags=lanczos,boxblur=18:2,eq=brightness=-0.25,setsar=1[bgimg];"
      f"[1:v][bgimg]overlay=0:0:shortest=1,"
      + dt("ROSHAN TPS", 700, 150, "white", font=FONT_N, start=0.1, fade=0.5) + ","
      + f"drawbox=x=390:y=890:w=300:h=8:color={ACCENT}:t=fill,"
      + dt("Built with Godot", 940, 56, "white", start=0.4) + ","
      + dt("Developer: Roshan", 1020, 56, ACCENT, start=0.6) + ","
      + dt("Personal derivative of the official Godot TPS demo", 1470, 30, "0xd0d7de", start=0.8) + ","
      + dt("Code MIT  ·  Assets CC BY 3.0 (Linietsky, Calabró)", 1515, 30, "0xd0d7de", start=0.8) + ","
      + dt("Music: Christian Fernando Perucchi (CC BY 3.0)", 1560, 30, "0xd0d7de", start=0.8)
      + "[v]")
segments.append(seg("s7", D, [["-loop", "1", "-framerate", str(FPS), "-t", str(D), "-i", still]], fc))

# ---- Assemble with crossfades -------------------------------------------------------------
inputs, chain, off, last = [], [], 0.0, "0:v"
for i, (p, d) in enumerate(segments):
    inputs += ["-i", p]
total = segments[0][1]
for i in range(1, len(segments)):
    off = total - XF
    lab = f"x{i}"
    chain.append(f"[{last}][{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[{lab}]")
    last = lab
    total = off + segments[i][1]
total = round(total, 3)
music = f"{GAME}/menu/menu_intro_music.ogg"
ai = len(segments)
chain.append(f"[{last}]fade=t=in:st=0:d=0.4,fade=t=out:st={total-0.6:.3f}:d=0.6,format=yuv420p[v]")
chain.append(f"[{ai}:a]atrim=0:{total},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-1.5:LRA=11,"
             f"afade=t=in:st=0:d=0.8,afade=t=out:st={total-1.5:.3f}:d=1.5,aresample=48000[a]")
run(["ffmpeg", "-loglevel", "error", "-y"] + inputs + ["-i", music,
     "-filter_complex", ";".join(chain), "-map", "[v]", "-map", "[a]",
     "-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-preset", "slow", "-crf", "19",
     "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "60",
     "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
     "-movflags", "+faststart", "-t", str(total), OUT])
print("TOTAL", total)
print(json.dumps([(os.path.basename(p), d) for p, d in segments]))
