"""
Genera og-card.jpg (1200x630) per daniferr.com
Esegui: python3 make_og.py
"""
from PIL import Image, ImageDraw, ImageFilter
import math, os

# ── Config ─────────────────────────────────────────────────────────────
W, H        = 1200, 630
BG          = (5,   5,   5)
ACCENT      = (77,  255, 163)
ACCENT_DIM  = (77,  255, 163, 30)
TEXT_BRIGHT = (232, 228, 220)
TEXT_DIM    = (90,  87,  80)
BORDER      = (200, 196, 188, 18)

PHOTO_SRC = os.path.join(os.path.dirname(__file__), "og-source.jpg")
OUT       = os.path.join(os.path.dirname(__file__), "og-card.jpg")

FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"

# ── Font loader ─────────────────────────────────────────────────────────
from PIL import ImageFont

def font(size):
    try:    return ImageFont.truetype(FONT_MONO, size)
    except: return ImageFont.load_default()

# ── Canvas ──────────────────────────────────────────────────────────────
card = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(card, "RGBA")

# ── Noise texture overlay (sottile) ─────────────────────────────────────
import random, struct
random.seed(42)
noise = Image.new("RGBA", (W, H), (0,0,0,0))
npx   = noise.load()
for y in range(H):
    for x in range(W):
        v = random.randint(0, 255)
        npx[x, y] = (v, v, v, random.randint(0, 6))
card.paste(Image.alpha_composite(card.convert("RGBA"), noise).convert("RGB"))
draw = ImageDraw.Draw(card, "RGBA")

# ── Photo (sinistra) ────────────────────────────────────────────────────
PHOTO_W = 420
if os.path.exists(PHOTO_SRC):
    photo = Image.open(PHOTO_SRC).convert("RGB")
    pw, ph = photo.size

    # Crop mezzo busto: prendi solo i 2/5 superiori dell'immagine
    # evitando il bicchiere (nella metà bassa) e le persone sullo sfondo
    crop_bottom = int(ph * 0.44)          # al 44% tagliamo → sopra il bicchiere
    crop_left   = int(pw * 0.05)          # 5% margin sinistra
    crop_right  = int(pw * 0.95)          # 5% margin destra
    photo = photo.crop((crop_left, 0, crop_right, crop_bottom))

    # Resize proporzionale a PHOTO_W x H con cover
    ratio    = max(PHOTO_W / photo.width, H / photo.height)
    new_size = (int(photo.width * ratio), int(photo.height * ratio))
    photo    = photo.resize(new_size, Image.LANCZOS)
    # Centra
    px = (PHOTO_W - photo.width)  // 2
    py = (H       - photo.height) // 2

    # Filtro cinematico (grayscale parziale + contrasto) — come nel sito
    gray     = photo.convert("L").convert("RGB")
    photo    = Image.blend(photo, gray, 0.65)          # 65% grigio
    # Aumenta contrasto moltiplicando
    enhancer_data = photo.getdata()
    brightened = [(min(255,int(r*1.1)), min(255,int(g*1.1)), min(255,int(b*1.1)))
                  for r,g,b in enhancer_data]
    photo.putdata(brightened)

    card.paste(photo, (px, py))

    # Gradiente verticale sopra la foto (fade bottom → dark)
    grad = Image.new("RGBA", (PHOTO_W, H), (0,0,0,0))
    gd   = ImageDraw.Draw(grad)
    for y in range(H):
        alpha = int(220 * (y / H) ** 1.8)
        gd.rectangle([(0, y), (PHOTO_W, y+1)], fill=(5, 5, 5, alpha))
    card.paste(Image.alpha_composite(card.convert("RGBA").crop((0,0,PHOTO_W,H)), grad).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(card, "RGBA")

    # Linea verticale accent tra foto e testo
    draw.rectangle([(PHOTO_W, 0), (PHOTO_W+1, H)], fill=(*ACCENT, 60))
else:
    # Placeholder se foto non trovata
    draw.rectangle([(0,0),(PHOTO_W,H)], fill=(13,13,13))
    draw.text((20, H//2), "→ salva la foto\ncome og-source.jpg", font=font(14), fill=TEXT_DIM)
    draw.rectangle([(PHOTO_W, 0), (PHOTO_W+1, H)], fill=(*ACCENT, 60))

# ── Area testo (destra) ─────────────────────────────────────────────────
TX  = PHOTO_W + 64   # left margin testo
TW  = W - TX - 48   # larghezza area testo

# Logo DF.
f_logo = font(52)
draw.text((TX, 64), "DF", font=f_logo, fill=TEXT_BRIGHT)
bbox = draw.textbbox((TX, 64), "DF", font=f_logo)
draw.text((bbox[2], 64), ".", font=f_logo, fill=ACCENT)

# Separatore accent
draw.rectangle([(TX, 148), (TX + 40, 149)], fill=ACCENT)

# Label
f_label = font(11)
draw.text((TX, 164), "DIGITAL STRATEGIST  ·  AI SPECIALIST", font=f_label, fill=TEXT_DIM)

# Nome grande
f_name = font(72)
name_y = 210
draw.text((TX, name_y), "DANILO", font=f_name, fill=TEXT_BRIGHT)
draw.text((TX, name_y + 82), "FERRANTE", font=f_name, fill=TEXT_BRIGHT)

# Tagline
f_tag = font(14)
tag_y = name_y + 190
draw.text((TX, tag_y),
          "Integro l'intelligenza artificiale\nnei processi che contano.",
          font=f_tag, fill=TEXT_DIM)

# URL accent
f_url = font(13)
url_y = H - 80
draw.text((TX, url_y), "daniferr.com", font=f_url, fill=ACCENT)

# Dot accent in basso a destra
cx, cy, cr = W - 52, H - 52, 6
draw.ellipse([(cx-cr, cy-cr), (cx+cr, cy+cr)], fill=ACCENT)
draw.ellipse([(cx-2,  cy-2),  (cx+2,  cy+2)],  fill=BG)

# Bordo esterno sottile
draw.rectangle([(0,0),(W-1,H-1)], outline=(*BORDER[:3], 80), width=1)

# ── Salva ───────────────────────────────────────────────────────────────
card.save(OUT, "JPEG", quality=92)
print(f"✅  og-card.jpg salvata → {OUT}")
