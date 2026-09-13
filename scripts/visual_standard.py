"""Small shared visual standard: logical 2200×1500, rendered at 2×."""
from pathlib import Path
import os

PAGE = (2200, 1500)
RENDER_SCALE = 2
PDF_POINTS = (792, 540)  # 11 × 7.5 inches, same 22:15 aspect as images
INK = '#172C3C'
BLUE = '#087DB0'
WARNING = '#C74A13'
MUTED = '#596976'
RULE = '#D4DDE3'
PALETTE_3D = {
    'new': (.02, .48, .72, 1), 'old': (.55, .60, .65, 1),
    'context': (.96, .97, .98, 1), 'hardware': (.09, .13, .17, 1),
    'arrow': (1, .28, .035, 1), 'white': (1, 1, 1, 1),
}

class Page:
    def __init__(self):
        from PIL import Image, ImageDraw
        self.im = Image.new('RGB', tuple(v * RENDER_SCALE for v in PAGE), 'white')
        self.draw = ImageDraw.Draw(self.im)

    def font(self, size, bold=False):
        from PIL import ImageFont
        directory = Path(os.environ.get('BH_FONT_DIR', 'C:/Windows/Fonts'))
        return ImageFont.truetype(str(directory / ('arialbd.ttf' if bold else 'arial.ttf')), round(size * RENDER_SCALE))

    def text(self, xy, text, size=28, fill=INK, bold=False, max_width=None):
        face = self.font(size, bold)
        if max_width is not None:
            assert self.draw.textlength(text, font=face) <= max_width * RENDER_SCALE, f'Label overflow: {text}'
        self.draw.text(tuple(round(v * RENDER_SCALE) for v in xy), text, font=face, fill=fill)

    def line(self, coords, fill=RULE, width=2):
        self.draw.line(tuple(round(v * RENDER_SCALE) for v in coords), fill=fill, width=width * RENDER_SCALE)

    def rect(self, coords, fill=None, outline=None, width=2):
        self.draw.rectangle(tuple(round(v * RENDER_SCALE) for v in coords), fill=fill, outline=outline, width=width * RENDER_SCALE)

    def polygon(self, points, fill):
        self.draw.polygon([(round(x * RENDER_SCALE), round(y * RENDER_SCALE)) for x, y in points], fill=fill)

    def image(self, path, rect):
        from PIL import Image
        im = Image.open(path).convert('RGBA')
        im.thumbnail((round(rect[2] * RENDER_SCALE), round(rect[3] * RENDER_SCALE)), Image.Resampling.LANCZOS)
        x = round(rect[0] * RENDER_SCALE + (rect[2] * RENDER_SCALE - im.width) / 2)
        y = round(rect[1] * RENDER_SCALE + (rect[3] * RENDER_SCALE - im.height) / 2)
        self.im.paste(im, (x, y), im)
        return (x / RENDER_SCALE, y / RENDER_SCALE, im.width / RENDER_SCALE, im.height / RENDER_SCALE)

    def warning(self, y, label, size=28):
        self.text((1410, y), label, size, WARNING, True, max_width=720)

    def footer(self, assembly, step):
        self.line((65, 1400, 2135, 1400))
        self.text((65, 1430), 'ILLUSTRATIVE — NOT TO SCALE', 23, MUTED)
        self.text((690, 1430), 'BOB BARROWS COMPANION PLANS CONTROL', 23, MUTED)
        self.text((1870, 1430), f'{assembly} · v2 / {step:02d}', 23, MUTED)

    def save(self, path):
        self.im.save(path, dpi=(400, 400))
