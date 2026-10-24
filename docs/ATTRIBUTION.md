# Attribution

ROSHAN TPS is a **modified derivative work** of the official
[Godot Third-Person Shooter demo](https://github.com/godotengine/tps-demo)
(upstream commit `a82f15448e9b015440d3bbdf5e10801b260c4e9f`, 2026-08-31).
It is **not** an original game built from scratch.

## Who made what

| Part | Author(s) | Licence | Changed in ROSHAN TPS? |
|---|---|---|---|
| Gameplay code (player, camera, enemies, level, menu, settings) | Juan Linietsky and the Godot Engine contributors (git history includes Aaron Franke, Hugo Locurcio, Rémi Verschelde, Clay John, QbieShay and others) | MIT | Minimal: one-word SSAO fix in `menu/settings.gd`, one branded text line in `level/debug.gd` |
| 3D models, textures, materials, animations, effects, title image, icon | Juan Linietsky, Fernando Miguel Calabró | CC BY 3.0 | **No** |
| Substance Painter source materials | GameTextures.com (as credited upstream) | as per upstream `LICENSE.md` | **No** |
| Music (`menu_intro_music.ogg`, `level_music.ogg`) | Christian Fernando Perucchi | CC BY 3.0 | **No** |
| PT Sans font | ParaType Ltd. | SIL OFL 1.1 | **No** |
| Engine | Godot Engine contributors | MIT | Not included / not modified |
| Text rebranding, SSAO fix, automated tests, CI workflow, documentation | **Roshan** (personal project developer/modifier) | MIT (code), same terms as upstream | New |

## CC BY 3.0 attribution statement

> "ROSHAN TPS" uses the assets and music of the *Godot Third-Person Shooter Demo*.
> Assets © 2018 Juan Linietsky, Fernando Miguel Calabró; music © 2018 Christian
> Fernando Perucchi; licensed under
> [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/legalcode).
> Source: <https://github.com/godotengine/tps-demo>.
> The assets have **not** been modified; the surrounding project has been
> modified (text rebranding, a settings bug fix, tests and documentation).
> No endorsement by the original authors or the Godot Foundation is implied.

## Where the credits appear

* [`LICENSE.md`](../LICENSE.md): upstream licence, unchanged.
* [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md): full notices.
* [`README.md`](../README.md): credits and licence section.
* In-game: the project has no credits screen upstream, and the text-only
  constraint prevented adding new scenes or nodes. The in-game branding is the
  window title ("ROSHAN TPS"), the loading text and the F3 overlay heading.
  The credits live in the repository documents above. Anyone who distributes an
  exported build should ship `LICENSE.md` and `THIRD_PARTY_NOTICES.md` with it.

## Trademarks

"Godot" and the Godot logo are trademarks of the Godot Foundation. They are used
here only to describe the engine the game runs on. ROSHAN TPS is a personal
project and is not affiliated with or endorsed by the Godot Foundation.
