"""Build the site's image assets from the engine repo's banner sources.

    /usr/bin/python3 tools/build_assets.py [path/to/mineru-assistant]

Writes into site/: emblem.webp (hero), morning-brief.webp (demo), og.jpg (link preview),
icon-512.png / apple-touch-icon.png / favicon-32.png / favicon.ico (the fox strokes on navy).
Needs Pillow and the `cwebp` binary (Homebrew `webp`).
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter

SITE_DIR = Path(__file__).resolve().parent.parent / "site"
DEFAULT_ENGINE_REPO = Path.home() / "Developer" / "mineru-assistant"

GROUND_RGB = (26, 24, 58)  # #1a183a, the banner's navy
EMBLEM_WIDTH_PX = 1040     # hero shows it at <= 520 CSS px, so this is 2x
DEMO_WIDTH_PX = 1440
OG_SIZE = (1200, 630)
ICON_MASTER_PX = 512
ICON_STROKE_SCALE = 0.86   # strokes fill most of the tile; the rest is breathing room
ICON_GLOW_BLUR_PX = 14
ICON_GLOW_OPACITY = 0.55
WEBP_QUALITY = 86


def write_webp(source_png: Path, output_webp: Path, width_px: int) -> None:
    """Resize to width_px (keeping aspect and alpha) and encode as WebP."""
    subprocess.run(
        ["cwebp", "-quiet", "-q", str(WEBP_QUALITY), "-alpha_q", "90", "-resize", str(width_px), "0",
         str(source_png), "-o", str(output_webp)],
        check=True,
    )


def write_link_preview(banner_png: Path, output_jpg: Path) -> None:
    """Scale the 16:9 banner to cover 1200x630 and centre-crop the overflow."""
    banner = Image.open(banner_png).convert("RGB")
    scale = max(OG_SIZE[0] / banner.width, OG_SIZE[1] / banner.height)
    scaled = banner.resize((round(banner.width * scale), round(banner.height * scale)), Image.LANCZOS)
    left = (scaled.width - OG_SIZE[0]) // 2
    top = (scaled.height - OG_SIZE[1]) // 2
    scaled.crop((left, top, left + OG_SIZE[0], top + OG_SIZE[1])).save(output_jpg, quality=88, optimize=True)


def render_icon_master(mask_png: Path, avatar_jpg: Path) -> Image.Image:
    """Solid fox strokes on navy: the stroke mask is the alpha, the avatar supplies each pixel's colour."""
    avatar = Image.open(avatar_jpg).convert("RGB")
    mask = Image.open(mask_png).convert("L").resize(avatar.size, Image.LANCZOS)
    strokes = avatar.copy()
    strokes.putalpha(mask)
    bounding_box = mask.getbbox()
    strokes = strokes.crop(bounding_box)

    stroke_px = round(ICON_MASTER_PX * ICON_STROKE_SCALE)
    scale = stroke_px / max(strokes.size)
    strokes = strokes.resize((round(strokes.width * scale), round(strokes.height * scale)), Image.LANCZOS)

    layer = Image.new("RGBA", (ICON_MASTER_PX, ICON_MASTER_PX), (0, 0, 0, 0))
    layer.paste(strokes, ((ICON_MASTER_PX - strokes.width) // 2, (ICON_MASTER_PX - strokes.height) // 2))
    glow = layer.filter(ImageFilter.GaussianBlur(ICON_GLOW_BLUR_PX))
    glow.putalpha(glow.getchannel("A").point(lambda alpha: round(alpha * ICON_GLOW_OPACITY)))

    icon = Image.new("RGBA", (ICON_MASTER_PX, ICON_MASTER_PX), GROUND_RGB + (255,))
    icon.alpha_composite(glow)
    icon.alpha_composite(layer)
    return icon.convert("RGB")


def main() -> None:
    """Build every asset; the engine repo path is the optional first argument."""
    engine_repo = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ENGINE_REPO
    banner_dir = engine_repo / "assets" / "banner"
    write_webp(banner_dir / "emblem.png", SITE_DIR / "emblem.webp", EMBLEM_WIDTH_PX)
    write_webp(engine_repo / "assets" / "demo" / "morning-brief.png", SITE_DIR / "morning-brief.webp", DEMO_WIDTH_PX)
    write_link_preview(banner_dir / "banner.png", SITE_DIR / "og.jpg")

    icon = render_icon_master(banner_dir / "mask.png", banner_dir / "logo_source.jpg")
    icon.save(SITE_DIR / "icon-512.png", optimize=True)
    icon.resize((180, 180), Image.LANCZOS).save(SITE_DIR / "apple-touch-icon.png", optimize=True)
    icon.resize((32, 32), Image.LANCZOS).save(SITE_DIR / "favicon-32.png", optimize=True)
    icon.save(SITE_DIR / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    for built in sorted(SITE_DIR.glob("*.*")):
        print(f"{built.stat().st_size:>8}  {built.name}")


if __name__ == "__main__":
    main()
