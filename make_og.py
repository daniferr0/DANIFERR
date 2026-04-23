"""
Genera og-card.jpg (1200x630) per daniferr.com
Esegui: python3 make_og.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, random

# ── Config ─────────────────────────────────────────────────────────────
W, H        = 1200, 630
BG          = (5,   5,   5)
ACCENT      = (77,  255, 163)
TEXT_BRIGHT = (232, 228, 220)
TEXT_DIM    = (90,  87,  80)

PHOTO_W  = 400          # larghezza colonna foto
TX       = PHOTO_W + 72  # x inizio testo
TW       = W - TX - 48   # larghezza area testo

PHOTO_SRC = os.path.join(os.path.dirname(__file__), "og-source.jpg")
OUT       = os.path.join(os.path.dirname(__file__), "og-card.jpg")
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"

def font(size):
    try:    return ImageFont.truetype(FONT_MONO, size)
    except: return ImageFont.load_default()

# ── Canvas base dark ────────────────────────────────────────────────────
card = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(card, "RGBA")

# ── Foto: crop mezzo busto → resize → crop esatto → filtro ─────────────
if os.path.exists(PHOTO_SRC):
    photo = Image.open(PHOTO_SRC).convert("RGB")
    pw, ph = photo.size

    # Crop mezzo busto: top 42% dell'immagine (testa + spalle, evita bicchiere)
    crop_top    = 0
    crop_bottom = int(ph * 0.42)
    crop_left   = int(pw * 0.08)
    crop_right  = int(pw * 0.92)
    photo = photo.crop((crop_left, crop_top, crop_right, crop_bottom))

    # Resize cover su area PHOTO_W x H
    ratio = max(PHOTO_W / photo.width, H / photo.height)
    nw    = int(photo.width  * ratio)
    nh    = int(photo.height * ratio)
    photo = photo.resize((nw, nh), Image.LANCZOS)

    # Crop centro esatto → PHOTO_W x H
    lx = (nw - PHOTO_W) // 2
    ty = (nh - H)        // 2
    photo = photo.crop((lx, ty, lx + PHOTO_W, ty + H))

    # Filtro cinematico (come nel sito)
    photo = ImageEnhance.Contrast(photo).enhance(1.18)
    photo = ImageEnhance.Brightness(photo).enhance(0.55)
    gray  = photo.convert("L").convert("RGB")
    photo = Image.blend(photo, gray, 0.72)   # 72% grigio

    card.paste(photo, (0, 0))

    # Overlay gradiente: fade verso destra (foto → sfondo scuro)
    fade = Image.new("RGBA", (PHOTO_W, H), (0, 0, 0, 0))
    fd   = ImageDraw.Draw(fade)
    for x in range(PHOTO_W):
        t     = x / (PHOTO_W - 1)
        alpha = int(255 * (t ** 1.6))      # forte sul bordo destro
        fd.rectangle([(x, 0), (x+1, H)], fill=(5, 5, 5, alpha))
    card.paste(Image.alpha_composite(photo.convert("RGBA"), fade).convert("RGB"), (0, 0))

    # Overlay gradiente: fade verso il basso
    draw2 = ImageDraw.Draw(card, "RGBA")
    for y in range(H // 2, H):
        t     = (y - H // 2) / (H // 2)
        alpha = int(160 * (t ** 2.0))
        draw2.rectangle([(0, y), (PHOTO_W, y+1)], fill=(5, 5, 5, alpha))

    draw = ImageDraw.Draw(card, "RGBA")

    # Linea accent verticale sottile
    draw.rectangle([(PHOTO_W - 1, 60), (PHOTO_W, H - 60)],
                   fill=(*ACCENT, 55))

# ── Testo (colonna destra) ──────────────────────────────────────────────

# Logo DF.
f_logo = font(48)
draw.text((TX, 58), "DF", font=f_logo, fill=TEXT_BRIGHT)
bb = draw.textbbox((TX, 58), "DF", font=f_logo)
draw.text((bb[2], 58), ".", font=f_logo, fill=ACCENT)

# Linea accent orizzontale
draw.rectangle([(TX, bb[3] + 16), (TX + 44, bb[3] + 17)], fill=ACCENT)

# Label ruolo
f_label = font(10)
draw.text((TX, bb[3] + 28), "DIGITAL STRATEGIST  ·  AI SPECIALIST",
          font=f_label, fill=TEXT_DIM)

# Nome — DANILO / FERRANTE
f_name = font(80)
ny     = bb[3] + 68
draw.text((TX, ny),        "DANILO",   font=f_name, fill=TEXT_BRIGHT)
draw.text((TX, ny + 90),   "FERRANTE", font=f_name, fill=TEXT_BRIGHT)

# Tagline
f_tag = font(13)
draw.text((TX, ny + 200),
          "Integro l'intelligenza artificiale\nnei processi che contano.",
          font=f_tag, fill=TEXT_DIM)

# URL in accent
f_url = font(12)
draw.text((TX, H - 72), "daniferr.com", font=f_url, fill=ACCENT)

# Dot accent decorativo
cx, cy, cr = W - 44, H - 44, 5
draw.ellipse([(cx - cr, cy - cr), (cx + cr, cy + cr)], fill=ACCENT)
draw.ellipse([(cx - 2,  cy - 2),  (cx + 2,  cy + 2)],  fill=BG)

# Bordo esterno
draw.rectangle([(0, 0), (W-1, H-1)], outline=(200, 196, 188, 22), width=1)

# ── Salva ───────────────────────────────────────────────────────────────
card.save(OUT, "JPEG", quality=94, optimize=True)
print(f"✅  og-card.jpg salvata → {OUT}")
