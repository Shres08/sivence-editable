"""Render a short Sivence motion storyboard from existing project artifacts."""
from pathlib import Path
import math
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "dist" / "assets"
OUT = Path(__file__).with_name("work-in-motion-study.mp4")
W, H, FPS, SEGMENT = 960, 540, 24, 2.3
DURATION = SEGMENT * 5
BLACK = (14, 15, 13)
WHITE = (245, 246, 240)
ORANGE = (255, 90, 31)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DISPLAY = str(ASSETS / "SivenceSans.ttf")


def f(size, display=False):
    return ImageFont.truetype(DISPLAY if display else FONT, size)


def ease(a, b, t):
    t = min(1, max(0, t))
    t = t * t * (3 - 2 * t)
    return a + (b - a) * t


def card(filename):
    image = Image.open(ASSETS / filename).convert("RGB")
    card_image = Image.new("RGBA", (760, 486), (233, 234, 230, 255))
    image.thumbnail((728, 450), Image.Resampling.LANCZOS)
    card_image.paste(image, ((760 - image.width) // 2, (486 - image.height) // 2))
    return card_image


def pair_card(first, second):
    page = Image.new("RGBA", (760, 486), (233, 234, 230, 255))
    for filename, left in ((first, 20), (second, 390)):
        item = Image.open(ASSETS / filename).convert("RGB")
        item.thumbnail((350, 448), Image.Resampling.LANCZOS)
        x = left + (350 - item.width) // 2
        page.paste(item, (x, (486 - item.height) // 2))
    return page


CARDS = [
    card("remic-audience-research.jpg"),
    pair_card("remic-paid-creatives.jpg", "remic-course-ad.webp"),
    pair_card("remic-fundmydream-post.webp", "remic-fundmydream-variant.webp"),
    pair_card("remic-career-fair.webp", "remic-event-team.webp"),
    card("remic-paid-performance.jpg"),
]


def project(source, quad):
    """Perspective project a real document into four screen corners."""
    sw, sh = source.size
    src = np.float64([[0, 0], [sw, 0], [sw, sh], [0, sh]])
    dst = np.float64(quad)
    rows = []
    rhs = []
    for (x, y), (u, v) in zip(dst, src):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); rhs.append(u)
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y]); rhs.append(v)
    a, b, c, d, e, ff, g, h = np.linalg.solve(np.array(rows), np.array(rhs))
    return source.transform((W, H), Image.Transform.PERSPECTIVE,
                            (a, b, c, d, e, ff, g, h),
                            resample=Image.Resampling.BICUBIC)


def draw_card(canvas, image, x, y, width, height, angle=0, alpha=255):
    skew = angle * width
    quad = [(x + skew, y + 6), (x + width - skew, y),
            (x + width + skew, y + height), (x - skew, y + height - 6)]
    warped = project(image, quad)
    mask = project(Image.new("RGBA", image.size, (255, 255, 255, alpha)), quad).getchannel("A")
    shadow = mask.filter(ImageFilter.GaussianBlur(18))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 130))
    canvas.alpha_composite(Image.composite(shade, Image.new("RGBA", (W, H)), shadow))
    warped.putalpha(mask)
    canvas.alpha_composite(warped)


def frame(t):
    canvas = Image.new("RGBA", (W, H), BLACK + (255,))
    d = ImageDraw.Draw(canvas)
    d.text((36, 32), "SIVENCE", font=f(17, True), fill=ORANGE)
    d.text((818, 35), "SELECTED WORK", font=f(10), fill=(165, 168, 158))
    d.line((36, 69, 924, 69), fill=(65, 68, 61), width=1)
    d.text((36, 101), "REMIC / FINANCIAL EDUCATION", font=f(11), fill=ORANGE)
    phase = min(4, int(t / SEGMENT))
    local = (t - phase * SEGMENT) / SEGMENT
    titles = ["Find the\naudience.", "Build the\nacquisition path.", "Give an idea\na campaign.", "Show up in\nthe market.", "Optimize with\nevidence."]
    details = ["Audience and journey research", "Course acquisition · paid creative", "Fund My Dream · campaign formats", "Career fair · industry activation", "Search and PMax performance"]
    labels = ["INSIGHT", "ACQUISITION", "CAMPAIGN", "ACTIVATION", "OPTIMIZATION"]
    outcome = ["Intent and audience mapping", "Search and Performance Max", "A separate campaign workstream", "Event creative and team presence", "2,260 tracked conversions"]
    d.multiline_text((36, 155), titles[phase], font=f(37, True), fill=WHITE, spacing=-3)
    d.text((37, 309), details[phase], font=f(15), fill=(190, 194, 183))
    d.text((37, 349), outcome[phase], font=f(14), fill=WHITE)
    if phase == 4:
        d.text((37, 373), "$35 cost per tracked conversion", font=f(14), fill=WHITE)
    d.rounded_rectangle((36, 438, 250, 480), radius=21, fill=ORANGE)
    d.text((56, 449), "EXPLORE REMIC CASE  ↗", font=f(12), fill=BLACK)

    # Each artifact advances toward the visitor, then yields to the next.
    cards = []
    for i in range(len(CARDS)):
        delta = i - phase
        if delta == 0:
            x, y, w, h, a, opacity = 415, 100, 500, 350, -.045, 255
            if local > .67 and phase < len(CARDS) - 1:
                u = (local - .67) / .33
                x, y, w, h = ease(x, 398, u), ease(y, 129, u), ease(w, 405, u), ease(h, 285, u)
                a = ease(a, .06, u)
        elif delta == 1:
            u = max(0, (local - .54) / .46)
            x, y, w, h = ease(851, 415, u), ease(156, 100, u), ease(290, 500, u), ease(205, 350, u)
            a, opacity = ease(.12, -.045, u), int(ease(185, 255, u))
        else:
            x, y, w, h, a, opacity = 925, 184, 250, 178, .16, 125
        cards.append((w * h, i, x, y, w, h, a, opacity))
    for _, i, x, y, w, h, a, opacity in sorted(cards, reverse=False):
        draw_card(canvas, CARDS[i], x, y, w, h, a, opacity)

    d = ImageDraw.Draw(canvas)
    d.rectangle((35, 510, 925, 511), fill=(65, 68, 61))
    d.rectangle((35, 510, 35 + int(890 * min(1, t / DURATION)), 513), fill=ORANGE)
    d.text((390, 481), f"{phase + 1:02d} / {len(CARDS):02d}   {labels[phase]}", font=f(10), fill=ORANGE)
    return canvas.convert("RGB")


def main():
    process = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "21",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT)
    ], stdin=subprocess.PIPE)
    for n in range(int(DURATION * FPS)):
        process.stdin.write(frame(n / FPS).tobytes())
    process.stdin.close()
    if process.wait():
        raise RuntimeError("ffmpeg failed")
    print(OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
