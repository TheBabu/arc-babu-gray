#!/usr/bin/env python3
"""Generate schematic theme previews (mock window + palette strip) as PNG.
Pure stdlib (zlib + struct) -- no external deps. Honest mockup using the
real arc-babu-gray colors, not a claimed screenshot."""
import zlib, struct, sys

def hx(h):
    h = h.lstrip('#')
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

# palette (dark variant)
BORDER  = hx('1c1c1c')
HEADER  = hx('2f2f2f')
BODY    = hx('282828')
SIDEBAR = hx('242424')
ENTRY   = hx('323232')
ACCENT  = hx('4278b7')
TEXT    = hx('d0d0d0')
SUBTEXT = hx('888888')
CLOSE   = hx('cc575d')
POLY    = hx('222222')   # polybar reference

class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = [list(bg) for _ in range(w*h)]
    def rect(self, x, y, w, h, c):
        for j in range(max(0,y), min(self.h, y+h)):
            base = j*self.w
            for i in range(max(0,x), min(self.w, x+w)):
                self.px[base+i] = list(c)
    def border(self, x, y, w, h, c, t=1):
        self.rect(x, y, w, t, c); self.rect(x, y+h-t, w, t, c)
        self.rect(x, y, t, h, c); self.rect(x+w-t, y, t, h, c)
    def png(self, path):
        raw = bytearray()
        for j in range(self.h):
            raw.append(0)
            row = self.px[j*self.w:(j+1)*self.w]
            for c in row:
                raw += bytes(c)
        comp = zlib.compress(bytes(raw), 9)
        def chunk(typ, data):
            return (struct.pack('>I', len(data)) + typ + data +
                    struct.pack('>I', zlib.crc32(typ+data) & 0xffffffff))
        with open(path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
            f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b'IDAT', comp))
            f.write(chunk(b'IEND', b''))

# ---- mock window preview on a polybar-colored backdrop ----
W, H = 720, 380
c = Canvas(W, H, POLY)
# top + bottom polybar strips (reference, to show separation)
c.rect(0, 0, W, 26, POLY)
c.rect(0, H-26, W, 26, POLY)
# a few polybar "module" ticks
for i, col in enumerate([TEXT, SUBTEXT, ACCENT]):
    c.rect(20 + i*22, 11, 12, 4, col)
c.rect(W-60, 11, 40, 4, SUBTEXT)

# window
wx, wy, ww, wh = 60, 56, 600, 268
c.border(wx-1, wy-1, ww+2, wh+2, BORDER, 2)        # window border vs polybar
# headerbar
c.rect(wx, wy, ww, 38, HEADER)
c.rect(wx, wy+38, ww, 1, BORDER)                   # header/body divider
# window title text + close button
c.rect(wx+14, wy+17, 120, 5, TEXT)
c.rect(wx+ww-26, wy+13, 12, 12, CLOSE)
# body
c.rect(wx, wy+39, ww, wh-39, BODY)
# sidebar
sbw = 150
c.rect(wx, wy+39, sbw, wh-39, SIDEBAR)
# sidebar rows; one selected (accent)
ry = wy+54
for k in range(6):
    if k == 1:
        c.rect(wx+8, ry-6, sbw-16, 22, ACCENT)
        c.rect(wx+18, ry, 90, 5, hx('ffffff'))
    else:
        c.rect(wx+18, ry, 70 + (k*7) % 50, 5, SUBTEXT if k % 2 else TEXT)
    ry += 30
# content area: an "entry" field + text lines + a button
cx = wx + sbw + 20
c.rect(cx, wy+58, 320, 26, ENTRY); c.border(cx, wy+58, 320, 26, BORDER, 1)
c.rect(cx+10, wy+69, 120, 5, SUBTEXT)
for k in range(5):
    c.rect(cx, wy+104 + k*22, 300 - (k*30) % 120, 5, TEXT if k % 2 == 0 else SUBTEXT)
# accent button (bottom-right)
c.rect(wx+ww-130, wy+wh-44, 110, 30, ACCENT)
c.rect(wx+ww-108, wy+wh-32, 66, 6, hx('ffffff'))
c.png(sys.argv[1] if len(sys.argv) > 1 else 'preview.png')

# ---- palette strip ----
labels = [BODY, ENTRY, HEADER, SIDEBAR, BORDER, TEXT, ACCENT, CLOSE]
sw, sh, pad = 84, 84, 0
p = Canvas(sw*len(labels), sh, (0,0,0))
for i, col in enumerate(labels):
    p.rect(i*sw, 0, sw, sh, col)
    p.border(i*sw, 0, sw, sh, hx('1a1a1a'), 1)
p.png((sys.argv[2] if len(sys.argv) > 2 else 'palette.png'))
print("wrote previews")
