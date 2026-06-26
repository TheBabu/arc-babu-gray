# Arc Babu Gray

A personal **neutral-gray** fork of the [Arc theme](https://github.com/jnsh/arc-theme),
recolored to match a gray polybar setup. Arc's blue-tinted greys are
neutralized to true gray, and the bright blue accent is replaced with a muted
gray-blue.

_Note: This theme was generated using Claude Code, using the Opus 4.8 model._

![Schematic preview of the Arc Babu Gray dark theme](.github/preview-dark.png)

> A schematic mockup (header, sidebar, selection, accent button, close button)
> rendered with the actual theme colors on a polybar-colored backdrop — not a
> live screenshot. Build and install to see it on real widgets.

## Palette (dark variant)

![Palette swatches](.github/palette.png)

| Role | Color | |
| --- | --- | --- |
| Window body (`bg_color`) | `#282828` | matches alacritty / rofi / dunst background |
| Entries, list views (`base_color`) | `#323232` | one step lighter than the body |
| Headerbar / titlebar (`header_bg`) | `#2f2f2f` | sits clearly above the `#222` polybar |
| Dark sidebar (`dark_sidebar_bg`) | `#242424` | |
| Window border | `#1c1c1c` | defines the window edge against the bars |
| Foreground / text | `#d0d0d0` | matches alacritty / rofi / dunst foreground |
| Accent / selection (`selected_bg_color`) | `#4278b7` | muted gray-blue |
| Window close button | `#cc575d` | kept red, in line with the dunst-critical red |

## Why these colors

* **Sourced from my dotfiles.** `#282828` background and `#d0d0d0` text come
  straight from my `alacritty`, `rofi` and `dunst` configs; the `#4278b7` accent
  is the muted gray-blue I'd already settled on in `arc-undead-custom`. The goal
  was a GTK theme that sits next to the terminal and bars without clashing.
* **No blending with the polybar.** Every window surface is kept *lighter* than
  the `#222` polybar — the darkest piece of window chrome is the `#2f2f2f`
  headerbar — and windows carry a `#1c1c1c` border. So a file manager (or any
  app) never merges into the top or bottom bars.
* **Everything else stays gray, consistently.** All the remaining greys across
  the theme — gradients, borders, scrollbars and the rendered widget assets —
  are neutralized the same way by `tools/recolor-gray.py`.
* **Semantic colors are left alone.** Warning / error / success, the red
  window-close button, and the GNOME / libadwaita named palette keep their
  meaning so apps still read correctly.

## Building and installing

The whole tree is already recolored, so just build the dark variant with Meson.
You only need the GTK themes, so restrict `-Dthemes` to avoid pulling in
Cinnamon/GNOME-Shell (Meson errors out probing for a Cinnamon version otherwise):

```bash
# deps (Arch): meson sassc glib2 inkscape
meson setup --prefix="$HOME/.local" -Dthemes=gtk2,gtk3,gtk4 -Dvariants=dark build/

# render assets single-threaded: Inkscape 1.x instances collide over DBus when
# run in parallel, so -j1 avoids random "Gio::DBus::Error" failures
ninja -C build/ -j1
meson install -C build/
```

This installs the theme as **`Arc-Babu-Gray`** into `~/.local/share/themes/`.

### Re-applying the recolor

The recolor is reproducible from one idempotent script, `tools/recolor-gray.py`,
which remaps colors across the SCSS sources, SVG asset sources and GTK2 `gtkrc`
files. The committed tree is already recolored; run it only if you reset to
upstream Arc or want to tweak the palette:

```bash
python3 tools/recolor-gray.py common
```

To tweak the palette, edit `EXPLICIT_OVERRIDE` in `tools/recolor-gray.py` (or the
`$bg_color` / `$selected_bg_color` etc. variables in `common/gtk-*/sass/_colors.scss`)
and rebuild. For example, to push the body darker toward the terminal, set
`bg_color` to `#222222`; to give it more separation from the polybar, raise it to
`#2c2c2c`.

## License

Arc is available under the terms of the GPL-3.0. See [COPYING](COPYING) for
details. Originally created by [horst3180](https://github.com/horst3180/arc-theme),
maintained upstream by [jnsh](https://github.com/jnsh/arc-theme).
