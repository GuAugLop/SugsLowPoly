#!/usr/bin/env python3
"""Builds the Sug's LowPoly publisher site:  python build.py   ->  ./docs  (the folder GitHub Pages publishes).

Edit site.json first:
  support_email        public support address shown on the contact page (required before going live)
  site_url             final address with a trailing slash, e.g. https://yourname.github.io/sugs-lowpoly/
                       (with your own domain, e.g. https://www.example.com/, the build also writes docs/CNAME)
  pack_store_url       Asset Store page of the pack; while empty the site shows "Coming soon"
  publisher_store_url  publisher page on the Asset Store (optional)
Needs only Python 3, no extra packages.
"""
import datetime
import html
import json
import os
import re
import shutil
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
OUT = os.path.join(HERE, "docs")   # GitHub Pages serves either the repository root or /docs

PAGES = {
    "index.html": dict(title="Sug's LowPoly | Game-ready low-poly assets for Unity",
                       description="Independent Unity Asset Store publisher of lightweight, stylized low-poly 3D packs with consistent pivots, real-world scale and specs you can check.",
                       canonical_path="", nav_home=True),
    "low-poly-enemy-melee-weapons.html": dict(title="Low Poly Enemy Melee Weapons | Sug's LowPoly",
                       description="50 low-poly melee weapons and shields for enemies, monsters and raiders. URP-ready Unity prefabs with grip-centered pivots, real-world scale and PBR textures.",
                       canonical_path="low-poly-enemy-melee-weapons.html", nav_pack=True),
    "contact.html": dict(title="Contact & support | Sug's LowPoly",
                       description="Customer support, bug reports and business enquiries for Sug's LowPoly asset packs.",
                       canonical_path="contact.html"),
    "privacy.html": dict(title="Privacy | Sug's LowPoly", description="This site sets no cookies and runs no trackers. How Sug's LowPoly handles the emails you send.",
                       canonical_path="privacy.html"),
    "404.html": dict(title="Page not found | Sug's LowPoly", description="This page does not exist.", canonical_path="404.html", noindex=True, is_404=True),
}

GALLERY = [
    ("01-key-art", "Key art: the enemy arsenal"),
    ("02-overview-all-weapons", "All 50 weapons and shields by category"),
    ("03-in-use-enemy-squad", "In use: grip-centered pivots on a humanoid rig"),
    ("04-enemy-armory", "Set dressing: an enemy armory"),
    ("05-sheet-swords", "Swords: 8 models"),
    ("06-sheet-axes", "Axes: 8 models"),
    ("07-sheet-blunt", "Blunt: 8 models"),
    ("08-sheet-polearms", "Polearms: 8 models"),
    ("09-sheet-improvised", "Improvised: 8 models"),
    ("10-sheet-monster", "Monster: 8 models"),
    ("11-sheet-shields", "Shields: 2 models, three views each"),
    ("12-true-to-scale", "True to scale against a 1.8 m humanoid"),
    ("13-clean-topology", "Clean low-poly topology"),
    ("14-stylized-pbr-materials", "Stylized PBR materials"),
    ("15-whats-inside", "What is inside the pack"),
]


def render(text, ctx, partials):
    text = re.sub(r"\{\{>\s*(\w+)\s*\}\}", lambda m: partials[m.group(1)], text)

    def cond(m):
        yes, _, no = m.group(2).partition("{{else}}")
        return yes if ctx.get(m.group(1)) else no
    text = re.sub(r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}", cond, text, flags=re.S)
    text = re.sub(r"\{\{\{(\w+)\}\}\}", lambda m: str(ctx.get(m.group(1), "")), text)
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: html.escape(str(ctx.get(m.group(1), "")), quote=True), text)
    return text


def main():
    cfg = json.load(open(os.path.join(HERE, "site.json"), encoding="utf-8"))
    pack = json.load(open(os.path.join(SRC, "data", "pack.json"), encoding="utf-8"))
    site_url = cfg.get("site_url", "").strip()
    if site_url and not site_url.endswith("/"):
        site_url += "/"
    email = cfg.get("support_email", "").strip()
    draft = not email
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        sys.exit("site.json: support_email does not look like an email address")

    partials = {n[:-5]: open(os.path.join(SRC, "partials", n), encoding="utf-8").read() for n in os.listdir(os.path.join(SRC, "partials"))}
    logo = open(os.path.join(SRC, "assets", "img", "logo-mark.svg"), encoding="utf-8").read().replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
    logo = re.sub(r' role="img" aria-label="[^"]*"', "", logo)

    gallery = "\n".join(
        f'        <li><a class="tile" href="assets/img/gallery/{slug}.webp" data-full="assets/img/gallery/{slug}.webp" data-caption="{html.escape(cap, quote=True)}">'
        f'<img src="assets/img/gallery/{slug}-thumb.webp" width="720" height="480" loading="lazy" alt="{html.escape(cap, quote=True)}"></a></li>'
        for slug, cap in GALLERY)
    categories = "\n".join(
        f'        <div class="cat"><h3>{html.escape(c["name"])} <span>{c["count"]}</span></h3><p>{html.escape(c["blurb"])} <span class="muted">{html.escape(", ".join(c["items"]))}.</span></p></div>'
        for c in pack["categories"])

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "icon-512.png"):
        shutil.copy(os.path.join(SRC, "root", name), os.path.join(OUT, name))

    base = dict(publisher=cfg.get("publisher", "Sug's LowPoly"), support_email=email, site_url=site_url,
                pack_store_url=cfg.get("pack_store_url", "").strip(), publisher_store_url=cfg.get("publisher_store_url", "").strip(),
                logo_svg=logo, gallery=gallery, categories=categories, updated=datetime.date.today().strftime("%B %d, %Y").replace(" 0", " "))
    for name, meta in PAGES.items():
        ctx = dict(base, **meta)
        ctx["noindex"] = bool(meta.get("noindex")) or draft
        ctx["base_tag"] = f'<base href="{html.escape(site_url, quote=True)}">\n' if (meta.get("is_404") and site_url) else ""
        page = render(open(os.path.join(SRC, "pages", name), encoding="utf-8").read(), ctx, partials)
        left = re.findall(r"\{\{[^}]*\}\}", page)
        if left:
            sys.exit(f"{name}: unresolved template tags {left[:3]}")
        open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(page)

    manifest = dict(name=base["publisher"], short_name="Sug's LowPoly", start_url="./", display="browser", background_color="#0b161e", theme_color="#0b161e",
                    icons=[dict(src="icon-512.png", sizes="512x512", type="image/png"), dict(src="apple-touch-icon.png", sizes="180x180", type="image/png")])
    json.dump(manifest, open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8"), indent=1)
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    # Custom domain: GitHub Pages reads it from a CNAME file inside the published folder. The build wipes docs/ every time,
    # so the file is written here whenever site_url is not a *.github.io address.
    host = (urlparse(site_url).hostname or "") if site_url else ""
    if host and not host.endswith(".github.io"):
        open(os.path.join(OUT, "CNAME"), "w", encoding="ascii", newline="\n").write(host + "\n")
    robots = "User-agent: *\n" + ("Disallow: /\n" if draft else "Allow: /\n") + (f"Sitemap: {site_url}sitemap.xml\n" if site_url and not draft else "")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(robots)
    if site_url and not draft:
        today = datetime.date.today().isoformat()
        urls = "".join(f"  <url><loc>{html.escape(site_url + m['canonical_path'])}</loc><lastmod>{today}</lastmod></url>\n" for n, m in PAGES.items() if not m.get("noindex"))
        open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")

    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print(f"built {len(PAGES)} pages -> {OUT}  ({size / 1e6:.1f} MB)")
    if draft:
        print("DRAFT BUILD: support_email is empty in site.json. The contact page shows a placeholder and search engines are told not to index. Do not publish this build.")
    if not site_url:
        print("note: site_url is empty, so canonical links, the social preview image and sitemap.xml were left out. Set it once you know the final address.")


if __name__ == "__main__":
    main()
