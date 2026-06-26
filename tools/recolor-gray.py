#!/usr/bin/env python3
"""Recolor Arc theme to a neutral-gray 'arc-babu-gray' palette.

Rules per 6-digit hex color:
  1. EXPLICIT_OVERRIDE  -> exact user-aligned value (key surfaces/text/accent)
  2. ACCENT_MAP         -> remap Arc's blue accent family to muted #4278b7 family
  3. low-saturation grey -> neutralize blue tint to true gray (keep lightness)
  4. otherwise          -> leave untouched (semantic/saturated colors)
"""
import os, re, sys

# --- user palette (from Dotfiles: alacritty/rofi/dunst + prior arc-undead-custom) ---
EXPLICIT_OVERRIDE = {
    # surfaces (dark variant)
    '383c4a': '282828',   # $bg_color        window body  (= user primary bg)
    '404552': '323232',   # $base_color      entries / list views (lighter)
    '2f343f': '2f2f2f',   # $header_bg       titlebar (elevated, clear of #222 polybar)
    '353945': '242424',   # $dark_sidebar_bg sidebars
    # foreground / text
    'd3dae3': 'd0d0d0',   # dark text/fg     (= user fg)
    '5c616c': '5c5c5c',   # light text/fg
    # surfaces (light variant)
    'f5f6f7': 'f5f5f5',   # $bg_color light
    'e7e8eb': 'e7e7e7',   # $header_bg light
    # accent
    '5294e2': '4278b7',   # $selected_bg_color  Arc blue -> muted gray-blue
    # Arc blue-grey chrome (scrollbar/shadow/border) whose spread > SPREAD_MAX escaped
    # auto-neutralize; neutralize them explicitly (leave saturated/semantic palette alone)
    '525d76': '5d5d5d', '5b627b': '636363', '5f6578': '656565',
    '5f697f': '686868', '70788d': '787878', 'b7c0d3': 'c0c0c0',
}

# accent family shades that appear (mostly) in rendered asset SVGs
ACCENT_MAP = {
    '66a1dc': '6a9bcf',   # lighter accent (checkbox/radio border highlight)
    'c0e3ff': 'c2d4e8',   # light accent tint (selection / check glow)
    '4dadd4': '4dadd4',   # $suggested_color: leave teal (semantic) -- explicit no-op
}

# colors we must NOT neutralize even though spread is small (already neutral, skip cost)
HEXRE = re.compile(r'#([0-9a-fA-F]{6})\b')

# semantic/saturated colors we never want neutralize to grab (extra safety allowlist)
KEEP = set()

SPREAD_MAX = 24   # max (maxchannel - minchannel) to count as a "chrome grey"

def luminance(r, g, b):
    return round(0.299*r + 0.587*g + 0.114*b)

def convert(hexstr):
    h = hexstr.lower()
    if h in EXPLICIT_OVERRIDE:
        return EXPLICIT_OVERRIDE[h]
    if h in ACCENT_MAP:
        return ACCENT_MAP[h]
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    spread = max(r,g,b) - min(r,g,b)
    if spread == 0:
        return None                      # already neutral grey, leave as-is
    if spread <= SPREAD_MAX and h not in KEEP:
        l = luminance(r, g, b)
        return f'{l:02x}{l:02x}{l:02x}'  # neutralize tint, keep lightness
    return None                          # saturated/semantic -> untouched

def process(path):
    with open(path, 'r', encoding='utf-8', errors='surrogateescape') as f:
        text = f.read()
    counts = {}
    def repl(m):
        orig = m.group(1)
        new = convert(orig)
        if new is None:
            return m.group(0)
        # preserve leading '#'
        counts[orig.lower()] = counts.get(orig.lower(), 0) + 1
        # keep original case style: output lowercase
        return '#' + new
    newtext = HEXRE.sub(repl, text)
    if newtext != text:
        with open(path, 'w', encoding='utf-8', errors='surrogateescape') as f:
            f.write(newtext)
    return counts

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else 'common'
    exts = ('.scss', '.svg', '.css', '.rc', '.xml')
    names = {'gtkrc'}
    total = {}
    files_changed = 0
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(exts) or fn in names:
                p = os.path.join(dirpath, fn)
                c = process(p)
                if c:
                    files_changed += 1
                    for k, v in c.items():
                        total[k] = total.get(k, 0) + v
    print(f"files changed: {files_changed}")
    print("top remapped source colors:")
    for k, v in sorted(total.items(), key=lambda kv: -kv[1])[:40]:
        print(f"  #{k} -> #{convert(k)}   x{v}")

if __name__ == '__main__':
    main()
