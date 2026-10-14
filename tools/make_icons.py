#!/usr/bin/env python3
"""Generate icon-192.png and icon-512.png for «سياق كرامات الأولياء».

Pure standard library (struct + zlib) — no Pillow needed. Renders a deep-green
square with a gold 8-point star (rub el hizb), matching icon.svg, with 4x
supersampling for smooth edges.
"""
import struct
import zlib

BG = (27, 67, 50)        # #1b4332
GOLD = (212, 175, 55)    # #d4af37
GOLD_A = 0.85            # border opacity


def in_rounded(px, py, size, inset, radius):
    left, top = inset, inset
    right, bottom = size - inset, size - inset
    if px < left or px > right or py < top or py > bottom:
        return False
    cx = min(max(px, left + radius), right - radius)
    cy = min(max(py, top + radius), bottom - radius)
    return (px - cx) ** 2 + (py - cy) ** 2 <= radius * radius


def sample_color(px, py, size):
    """Return (r,g,b) for a point in pixel space, or None for transparent."""
    c = size / 2.0
    rx, ry = px - c, py - c
    scale = size / 512.0
    R = 164 * scale          # star tip radius

    # 8-point star = diamond (|x|+|y|<=R) U axis-square (max(|x|,|y|)<=R/sqrt2)
    diamond = abs(rx) + abs(ry) <= R
    square = max(abs(rx), abs(ry)) <= R / 1.41421356
    star = diamond or square

    # center disc + gold pin
    disc = rx * rx + ry * ry <= (40 * scale) ** 2
    pin = rx * rx + ry * ry <= (16 * scale) ** 2

    border = in_rounded(px, py, size, 14 * scale, 92 * scale) and \
        not in_rounded(px, py, size, 23 * scale, 83 * scale)

    col = BG
    if border:
        col = tuple(int(GOLD_A * g + (1 - GOLD_A) * b) for g, b in zip(GOLD, BG))
    if star:
        col = GOLD
    if disc:
        col = BG
    if pin:
        col = GOLD
    return col


def render(size, ss=4):
    rows = []
    for y in range(size):
        row = bytearray()
        for x in range(size):
            r = g = b = 0
            for sy in range(ss):
                for sx in range(ss):
                    col = sample_color(x + (sx + 0.5) / ss, y + (sy + 0.5) / ss, size)
                    r += col[0]; g += col[1]; b += col[2]
            n = ss * ss
            row += bytes((r // n, g // n, b // n, 255))
        rows.append(bytes(row))
    return b''.join(b'\x00' + r for r in rows)


def write_png(path, size, ss=4):
    raw = render(size, ss)
    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data +
                struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) +
           chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)
    print('wrote', path, size, 'x', size, len(png), 'bytes')


if __name__ == '__main__':
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    base = os.path.dirname(here)
    write_png(os.path.join(base, 'icon-192.png'), 192)
    write_png(os.path.join(base, 'icon-512.png'), 512)
