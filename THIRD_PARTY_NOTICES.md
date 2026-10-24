# Third-Party Notices

**ROSHAN TPS** is a personal, modified derivative of the official
**Godot Third-Person Shooter demo** (<https://github.com/godotengine/tps-demo>,
upstream commit `a82f15448e9b015440d3bbdf5e10801b260c4e9f`).
Nearly all code, every 3D asset, texture, animation, sound, music track and the
title image were created by the upstream authors listed below. Roshan's
contribution is the personal text rebranding, a settings bug fix, an automated
test suite, CI and documentation (see `docs/CHANGES_FROM_UPSTREAM.md`).

The upstream [`LICENSE.md`](LICENSE.md) is kept **unchanged** in this repository
and is the authoritative statement. Its terms are summarised here.

---

## 1. Game code — MIT License

All code Copyright (c) 2018-2021 Juan Linietsky, Godot Engine contributors.
Modifications Copyright (c) 2026 Roshan, under the same MIT terms.

```
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## 2. 3D assets, textures, animations and other art — CC BY 3.0

All assets Copyright (c) 2018 **Juan Linietsky, Fernando Miguel Calabró**.
Distributed under the Creative Commons Attribution License version 3.0
(CC BY 3.0) — <https://creativecommons.org/licenses/by/3.0/legalcode>.

Existing as derivative work, many original Substance Painter materials used to
create this scene were kindly provided by **GameTextures.com**.

The assets are redistributed **unmodified** in ROSHAN TPS (no image, model,
material, animation, audio, font or shader file was changed).

## 3. Music — CC BY 3.0

Music Copyright (c) 2018 **Christian Fernando Perucchi**.
Distributed under CC BY 3.0 — <https://creativecommons.org/licenses/by/3.0/legalcode>.
Files: `menu/menu_intro_music.ogg`, `level/level_music.ogg` (unmodified).

## 4. Font — SIL Open Font License 1.1

**PT Sans** — Copyright (c) 2010, ParaType Ltd. (<http://www.paratype.com/public>),
with Reserved Font Names "PT Sans" and "ParaType".
Licensed under the SIL Open Font License, Version 1.1. Full text:
[`menu/font/OFL.txt`](menu/font/OFL.txt) (unmodified). File:
`menu/font/PT_Sans-Web-Bold.ttf` (unmodified).

## 5. Godot Engine — MIT License

ROSHAN TPS runs on the Godot Engine (<https://godotengine.org>), which is
not included in this repository. The engine is
Copyright (c) 2014-present Godot Engine contributors and
Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur, and is distributed under the
MIT License. Exported builds of the game embed the engine and its third-party
components; their notices are listed at
<https://godotengine.org/license/> and in the engine's
`COPYRIGHT.txt` / `Engine.get_license_info()`. Any exported build you share
must include these notices.

## 6. Upstream branding that remains in the game

As required for this project, the rebranding is **text-only**: no image assets
were replaced. The following upstream/engine visuals therefore remain and are
**not** claimed as Roshan's work:

* the main-menu title image `menu/tps_demo.png` (reads "TPS Demo");
* the upstream project/window icon `icon.png` (a render of the demo's robot, CC BY 3.0);
* the Godot Engine boot splash shown while the engine starts.
