import math
import struct
import zlib

PALETTE = [
    (16, 4, 6),
    (70, 8, 18),
    (178, 16, 52),
    (255, 45, 85),
    (255, 120, 140),
    (255, 214, 220),
]

INTERIOR = (10, 3, 4)

VIEWS = {
    "small": {"cols": 58, "rows": 16, "max_iter": 100},
    "medium": {"cols": 88, "rows": 24, "max_iter": 140},
    "large": {"cols": 116, "rows": 32, "max_iter": 180},
}

VIEW_CENTER = (-0.7, 0.0)
VIEW_WIDTH = 3.0
SUPERSAMPLE = 4


def _smooth(cre, cim, max_iter, bail=4.0):
    x = 0.0
    y = 0.0
    x2 = 0.0
    y2 = 0.0
    i = 0
    while x2 + y2 <= bail and i < max_iter:
        y = 2.0 * x * y + cim
        x = x2 - y2 + cre
        x2 = x * x
        y2 = y * y
        i += 1
    if i >= max_iter:
        return None
    log_zn = math.log(x2 + y2) / 2.0
    nu = math.log(log_zn / math.log(2.0)) / math.log(2.0)
    return (i + 1 - nu) / max_iter


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _color(t):
    t = max(0.0, min(1.0, t))
    scaled = t * (len(PALETTE) - 1)
    idx = min(int(scaled), len(PALETTE) - 2)
    frac = scaled - idx
    return _lerp(PALETTE[idx], PALETTE[idx + 1], frac)


def fractal_pixels(cols, rows, max_iter, view_center=None, view_width=None):
    if view_center is None:
        view_center = VIEW_CENTER
    if view_width is None:
        view_width = VIEW_WIDTH
    cx, cy = view_center
    height = view_width * rows / cols
    xmin = cx - view_width / 2
    xmax = cx + view_width / 2
    ymin = cy - height / 2
    ymax = cy + height / 2

    ss = SUPERSAMPLE
    pixels = []
    for py in range(rows):
        row = []
        for px in range(cols):
            acc = [0, 0, 0]
            inside = 0
            for sy in range(ss):
                fy = (py + (sy + 0.5) / ss) / rows
                cim = ymax - fy * (ymax - ymin)
                for sx in range(ss):
                    fx = (px + (sx + 0.5) / ss) / cols
                    cre = xmin + fx * (xmax - xmin)
                    t = _smooth(cre, cim, max_iter)
                    if t is None:
                        inside += 1
                        continue
                    c = _color(t)
                    acc[0] += c[0]
                    acc[1] += c[1]
                    acc[2] += c[2]
            total = ss * ss
            if inside == total:
                row.append(INTERIOR)
            elif inside > 0:
                n = total - inside
                row.append(
                    (
                        (acc[0] + INTERIOR[0] * inside) // total,
                        (acc[1] + INTERIOR[1] * inside) // total,
                        (acc[2] + INTERIOR[2] * inside) // total,
                    )
                )
            else:
                row.append((acc[0] // total, acc[1] // total, acc[2] // total))
        pixels.append(row)
    return pixels


def render_halfblock(pixels, cols, rows):
    lines = []
    for r in range(rows):
        row = []
        for c in range(cols):
            top = pixels[2 * r][c]
            bot = pixels[2 * r + 1][c]
            if top == bot:
                row.append(f"\x1b[38;2;{top[0]};{top[1]};{top[2]}m▀")
            else:
                row.append(
                    f"\x1b[38;2;{top[0]};{top[1]};{top[2]}m"
                    f"\x1b[48;2;{bot[0]};{bot[1]};{bot[2]}m▀"
                )
        lines.append("".join(row) + "\x1b[0m")
    return "\n".join(lines)


def render_ascii(pixels, cols, rows):
    ramp = " .:-=+*#%@"
    lines = []
    for r in range(rows):
        line = []
        for c in range(cols):
            top = pixels[2 * r][c]
            bot = pixels[2 * r + 1][c]
            lum_top = 0.299 * top[0] + 0.587 * top[1] + 0.114 * top[2]
            lum_bot = 0.299 * bot[0] + 0.587 * bot[1] + 0.114 * bot[2]
            lum = (lum_top + lum_bot) / 2 / 255
            line.append(ramp[int(lum * (len(ramp) - 1))])
        lines.append("".join(line))
    return "\n".join(lines)


def build(size="small"):
    view = VIEWS.get(size, VIEWS["small"])
    cols = view["cols"]
    rows = view["rows"]
    max_iter = view["max_iter"]
    pixels = fractal_pixels(cols, rows * 2, max_iter)
    return render_halfblock(pixels, cols, rows)


def write_png(path, pixels):
    height = len(pixels)
    width = len(pixels[0]) if height else 0
    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for r, g, b in row:
            raw.extend((r, g, b))

    def chunk(tag, data):
        payload = tag + data
        return (
            struct.pack(">I", len(data))
            + payload
            + struct.pack(">I", zlib.crc32(payload))
        )

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
        + chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)
