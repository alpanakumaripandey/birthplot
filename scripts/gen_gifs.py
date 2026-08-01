"""Generate small looping GIFs for Birthplot (teal/brass monsoon-ink palette)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "web" / "public" / "art"
OUT.mkdir(parents=True, exist_ok=True)

JADE = (61, 181, 173, 255)
BRASS = (166, 124, 61, 255)
MIST = (210, 226, 230, 40)
INK = (26, 36, 40, 255)


def _frame(size: int, bg=(14, 22, 26, 255)) -> Image.Image:
    return Image.new("RGBA", (size, size), bg)


def twinkle_sky(path: Path, size: int = 320, frames: int = 16) -> None:
    imgs = []
    stars = [
        (40, 50, 1.2),
        (90, 30, 0.9),
        (160, 70, 1.5),
        (220, 40, 1.0),
        (280, 90, 1.3),
        (60, 140, 0.8),
        (130, 180, 1.1),
        (200, 150, 0.7),
        (260, 200, 1.4),
        (100, 250, 1.0),
        (180, 260, 0.9),
        (250, 280, 1.2),
        (300, 160, 0.8),
        (30, 220, 1.1),
        (150, 120, 1.0),
    ]
    for i in range(frames):
        im = _frame(size)
        d = ImageDraw.Draw(im)
        t = i / frames * math.tau
        # soft nebula wash
        for cx, cy, r in ((size // 2, size // 2, 90), (80, 200, 50), (240, 80, 45)):
            pulse = 0.35 + 0.15 * math.sin(t + cx * 0.01)
            col = (61, 181, 173, int(40 * pulse))
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        for sx, sy, base in stars:
            a = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 2 + sx * 0.05 + sy * 0.03))
            rad = max(1, int(base * (1.2 + a)))
            alpha = int(80 + 175 * a)
            d.ellipse(
                (sx - rad, sy - rad, sx + rad, sy + rad),
                fill=(210, 226, 230, alpha),
            )
            if a > 0.75:
                d.line((sx - rad * 2, sy, sx + rad * 2, sy), fill=(166, 124, 61, 120), width=1)
                d.line((sx, sy - rad * 2, sx, sy + rad * 2), fill=(166, 124, 61, 120), width=1)
        imgs.append(im.convert("P", palette=Image.ADAPTIVE, colors=64))
    imgs[0].save(
        path,
        save_all=True,
        append_images=imgs[1:],
        duration=90,
        loop=0,
        optimize=True,
    )


def orbit_ring(path: Path, size: int = 240, frames: int = 24) -> None:
    imgs = []
    for i in range(frames):
        im = _frame(size, (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx = cy = size // 2
        # diamond
        diamond = [(cx, cy - 36), (cx + 36, cy), (cx, cy + 36), (cx - 36, cy)]
        d.polygon(diamond, outline=BRASS[:3] + (220,), width=2)
        d.polygon([(cx, cy - 20), (cx + 20, cy), (cx, cy + 20), (cx - 20, cy)], fill=JADE[:3] + (50,))
        ang = i / frames * math.tau
        for k, (radius, color) in enumerate(((70, JADE), (88, BRASS), (105, MIST))):
            a = ang + k * (math.tau / 3)
            x = cx + math.cos(a) * radius
            y = cy + math.sin(a) * radius
            r = 5 if k == 0 else 3
            d.ellipse((x - r, y - r, x + r, y + r), fill=color[:3] + (230,))
        imgs.append(im.convert("P", palette=Image.ADAPTIVE, colors=48))
    imgs[0].save(
        path,
        save_all=True,
        append_images=imgs[1:],
        duration=70,
        loop=0,
        optimize=True,
        transparency=0,
        disposal=2,
    )


def ink_pulse(path: Path, size: int = 180, frames: int = 14) -> None:
    imgs = []
    for i in range(frames):
        im = _frame(size, (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx = cy = size // 2
        # expand then fade
        phase = i / (frames - 1)
        r = int(12 + phase * 60)
        alpha = int(200 * (1 - phase))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=JADE[:3] + (alpha,), width=3)
        r2 = int(8 + phase * 40)
        d.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), outline=BRASS[:3] + (alpha // 2,), width=2)
        d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=BRASS[:3] + (220,))
        imgs.append(im.convert("P", palette=Image.ADAPTIVE, colors=32))
    imgs[0].save(
        path,
        save_all=True,
        append_images=imgs[1:],
        duration=80,
        loop=0,
        optimize=True,
        transparency=0,
        disposal=2,
    )


def main() -> None:
    twinkle_sky(OUT / "loop-nakshatra.gif")
    orbit_ring(OUT / "loop-orbit.gif")
    ink_pulse(OUT / "loop-ink.gif")
    print("wrote", list(OUT.glob("loop-*.gif")))


if __name__ == "__main__":
    main()
