import struct
import zlib

ACCENT = (34, 211, 238)
BG = (7, 10, 18)

VIEWS = {
    "small": {"cols": 58, "rows": 16, "max_iter": 90},
    "medium": {"cols": 86, "rows": 22, "max_iter": 110},
    "large": {"cols": 112, "rows": 30, "max_iter": 130},
}

VIEW_CENTER = (-0.7, 0.0)
VIEW_WIDTH = 3.0


def _in_set(cre, cim, max_iter, bail=4.0):
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
    return i >= max_iter


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

    pixels = []
    for py in range(rows):
        cim = ymax - (py + 0.5) / rows * (ymax - ymin)
        row = []
        for px in range(cols):
            cre = xmin + (px + 0.5) / cols * (xmax - xmin)
            row.append(ACCENT if _in_set(cre, cim, max_iter) else BG)
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
    lines = []
    for r in range(rows):
        line = []
        for c in range(cols):
            top = pixels[2 * r][c]
            bot = pixels[2 * r + 1][c]
            lit_top = 1 if top == ACCENT else 0
            lit_bot = 1 if bot == ACCENT else 0
            line.append("#" if lit_top + lit_bot >= 1 else " ")
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
