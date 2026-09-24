#!/usr/bin/env python3
"""Builds the Sug's LowPoly publisher site:  python build.py   ->  ./docs  (the folder GitHub Pages publishes).

Edit site.json first:
  support_email        public support address shown on the contact page (required before going live)
  site_url             final address with a trailing slash, e.g. https://yourname.github.io/sugs-lowpoly/
                       (with your own domain, e.g. https://www.example.com/, the build also writes docs/CNAME)
  store_urls           Asset Store link of each pack, keyed by the pack's slug; while a link is empty
                       that pack shows "Coming soon"
  pack_store_url       older single-pack setting, still read for the pack whose data file has "uses_pack_store_url": true
                       (Low Poly Enemy Melee Weapons) when its entry in store_urls is empty
  publisher_store_url  publisher page on the Asset Store (optional)

Each pack is one file in src/data/packs/<slug>.json. Its page, <slug>.html, is rendered from src/templates/pack.html,
and the pack also gets a card on the home page, links in the header and footer, and a sitemap entry.
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
PACKS_DIR = os.path.join(SRC, "data", "packs")

# Pages written by hand in src/pages. The pack pages are added after the home page, one per file in src/data/packs.
PAGES = {
    "index.html": dict(title="Sug's LowPoly | Game-ready low-poly assets for Unity",
                       description="Independent Unity Asset Store publisher of lightweight, stylized low-poly 3D packs with consistent pivots, real-world scale and specs you can check.",
                       canonical_path="", nav_home=True),
    "contact.html": dict(title="Contact & support | Sug's LowPoly",
                       description="Customer support, bug reports and business enquiries for Sug's LowPoly asset packs.",
                       canonical_path="contact.html"),
    "privacy.html": dict(title="Privacy | Sug's LowPoly", description="This site sets no cookies and runs no trackers. How Sug's LowPoly handles the emails you send.",
                       canonical_path="privacy.html"),
    "404.html": dict(title="Page not found | Sug's LowPoly", description="This page does not exist.", canonical_path="404.html", noindex=True, is_404=True),
}
DEFAULT_OG_IMAGE = "assets/img/og-image.jpg"
PACK_KEYS = ("order", "slug", "name", "short_name", "nav_label", "faq_label", "title", "description", "images", "hero", "facts", "overview_html",
             "checks_html", "gallery", "contents_title_html", "categories", "specs", "compat", "faq", "card")


def render(text, ctx, partials):
    text = re.sub(r"\{\{>\s*(\w+)\s*\}\}", lambda m: partials[m.group(1)], text)

    def cond(m):
        yes, _, no = m.group(2).partition("{{else}}")
        return yes if ctx.get(m.group(1)) else no

    def value(m):
        if m.group(1) not in ctx:
            raise KeyError(f"template uses {{{{{m.group(1)}}}}} but the build has no value for it")
        return str(ctx[m.group(1)])
    text = re.sub(r"\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}", cond, text, flags=re.S)
    text = re.sub(r"\{\{\{(\w+)\}\}\}", value, text)
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: html.escape(value(m), quote=True), text)
    return text


def esc(s):
    return html.escape(s, quote=True)


def load_packs(cfg):
    """Reads src/data/packs/*.json, checks them and resolves each pack's store link."""
    store_urls = cfg.get("store_urls") or {}
    packs = []
    for fn in sorted(os.listdir(PACKS_DIR)):
        if not fn.endswith(".json"):
            continue
        p = json.load(open(os.path.join(PACKS_DIR, fn), encoding="utf-8"))
        missing = [k for k in PACK_KEYS if k not in p]
        if missing:
            sys.exit(f"src/data/packs/{fn}: missing {', '.join(missing)}")
        if fn != p["slug"] + ".json":
            sys.exit(f"src/data/packs/{fn}: the file name must be the slug ({p['slug']}.json)")
        url = (store_urls.get(p["slug"]) or "").strip()
        if not url and p.get("uses_pack_store_url"):
            url = (cfg.get("pack_store_url") or "").strip()
        p["resolved_store_url"] = url or (p.get("store_url") or "").strip()
        img = p["images"]
        need = [img["card"], img.get("og") or DEFAULT_OG_IMAGE]
        for slug, _ in p["gallery"]["images"]:
            need += [f"{img['gallery_dir']}/{slug}.webp", f"{img['gallery_dir']}/{slug}-thumb.webp"]
        absent = [n for n in need if not os.path.isfile(os.path.join(SRC, *n.split("/")))]
        if absent:
            sys.exit(f"src/data/packs/{fn}: image not found in src/: {absent[0]}" + (f" (and {len(absent) - 1} more)" if len(absent) > 1 else ""))
        packs.append(p)
    packs.sort(key=lambda p: (p["order"], p["slug"]))
    unknown = [s for s in store_urls if s not in {p["slug"] for p in packs}]
    if unknown:
        sys.exit(f"site.json: store_urls has a link for {unknown[0]}, but there is no src/data/packs/{unknown[0]}.json")
    return packs


def pack_card(p, partials):
    """The card used on the home page and in the "Pairs well with" section of the other pack pages."""
    c = p["card"]
    facts = "\n".join(f"            <li><b>{b}</b><span>{s}</span></li>" for b, s in c["facts"])
    ctx = dict(slug=p["slug"], name=p["name"], store_url=p["resolved_store_url"], card_image=p["images"]["card"], card_alt=c["image_alt"],
               card_eyebrow=c["eyebrow_html"], card_blurb=c["blurb_html"], card_facts=facts)
    return render(partials["pack_card"], ctx, partials).rstrip("\n")


def pack_page_ctx(p, by_slug, partials):
    img, hero, gal = p["images"], p["hero"], p["gallery"]
    gallery = "\n".join(
        f'        <li><a class="tile" href="{img["gallery_dir"]}/{slug}.webp" data-full="{img["gallery_dir"]}/{slug}.webp" data-caption="{esc(cap)}">'
        f'<img src="{img["gallery_dir"]}/{slug}-thumb.webp" width="720" height="480" loading="lazy" alt="{esc(cap)}"></a></li>'
        for slug, cap in gal["images"])
    categories = "\n".join(
        f'        <div class="cat"><h3>{html.escape(c["name"])} <span>{c["count"]}</span></h3><p>{html.escape(c["blurb"])} <span class="muted">{html.escape(", ".join(c["items"]))}.</span></p></div>'
        for c in p["categories"])
    pair = ""
    if p.get("pairs_with"):
        other = by_slug.get(p["pairs_with"]["slug"])
        if not other:
            sys.exit(f"{p['slug']}: pairs_with points to {p['pairs_with']['slug']}, which has no data file")
        pair = ('  <section class="pair" aria-labelledby="pair-title">\n    <div class="wrap">\n      <div class="section-head">\n'
                '        <p class="eyebrow">Pairs well with</p>\n'
                f'        <h2 class="display" id="pair-title">{p["pairs_with"]["title_html"]}</h2>\n'
                f'        <p class="lead">{p["pairs_with"]["lead_html"]}</p>\n      </div>\n'
                f'{pack_card(other, partials)}\n    </div>\n  </section>\n\n')
    return dict(
        title=p["title"], description=p["description"], canonical_path=p["slug"] + ".html", nav_slug=p["slug"],
        og_image=img.get("og") or DEFAULT_OG_IMAGE,
        page_head_class="page-head with-art" + (" " + img["banner_class"] if img.get("banner_class") else ""),
        short_name=p["short_name"], store_url=p["resolved_store_url"], name_html=hero["name_html"], lead_html=hero["lead_html"],
        hero_note=f'      <p class="small muted">{hero["note_html"]}</p>\n' if hero.get("note_html") else "",
        facts="\n".join(f"        <li><b>{b}</b><span>{s}</span></li>" for b, s in p["facts"]),
        overview="\n".join(f"          <p>{t}</p>" for t in p["overview_html"]),
        checks="\n".join(f"          <li>{t}</li>" for t in p["checks_html"]),
        gallery_title=gal["title_html"], gallery_lead=gal["lead_html"], gallery_note=gal["note_html"], gallery=gallery,
        contents_title=p["contents_title_html"], categories=categories,
        specs="\n".join(f'            <tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in p["specs"]),
        compat_eyebrow=p["compat"]["eyebrow_html"], compat_title=p["compat"]["title_html"],
        compat="\n".join(f"        <p>{t}</p>" for t in p["compat"]["paragraphs_html"]),
        faq="\n".join(f'        <details>\n          <summary>{q}</summary>\n          <div class="answer">{a}</div>\n        </details>' for q, a in p["faq"]),
        pair_section=pair,
    )


def main():
    cfg = json.load(open(os.path.join(HERE, "site.json"), encoding="utf-8"))
    site_url = cfg.get("site_url", "").strip()
    if site_url and not site_url.endswith("/"):
        site_url += "/"
    email = cfg.get("support_email", "").strip()
    draft = not email
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        sys.exit("site.json: support_email does not look like an email address")

    partials = {n[:-5]: open(os.path.join(SRC, "partials", n), encoding="utf-8").read() for n in os.listdir(os.path.join(SRC, "partials")) if n.endswith(".html")}
    logo = open(os.path.join(SRC, "assets", "img", "logo-mark.svg"), encoding="utf-8").read().replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
    logo = re.sub(r' role="img" aria-label="[^"]*"', "", logo)
    pack_tpl = open(os.path.join(SRC, "templates", "pack.html"), encoding="utf-8").read()

    packs = load_packs(cfg)
    by_slug = {p["slug"]: p for p in packs}
    for p in packs:
        if p["slug"] + ".html" in PAGES or os.path.exists(os.path.join(SRC, "pages", p["slug"] + ".html")):
            print(f"note: src/pages/{p['slug']}.html is no longer used; the page is built from src/templates/pack.html and "
                  f"src/data/packs/{p['slug']}.json. The old file can be deleted.")
    if os.path.exists(os.path.join(SRC, "data", "pack.json")):
        print("note: src/data/pack.json is no longer used; pack data lives in src/data/packs/. The old file can be deleted.")

    # Page list: home, then one page per pack, then the other hand-written pages.
    pages = [("index.html", PAGES["index.html"], None)]
    pages += [(p["slug"] + ".html", pack_page_ctx(p, by_slug, partials), pack_tpl) for p in packs]
    pages += [(n, m, None) for n, m in PAGES.items() if n != "index.html"]

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
    for name in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "icon-512.png"):
        shutil.copy(os.path.join(SRC, "root", name), os.path.join(OUT, name))

    def and_list(items):
        return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]

    base = dict(publisher=cfg.get("publisher", "Sug's LowPoly"), support_email=email, site_url=site_url,
                publisher_store_url=cfg.get("publisher_store_url", "").strip(), og_image=DEFAULT_OG_IMAGE,
                logo_svg=logo, updated=datetime.date.today().strftime("%B %d, %Y").replace(" 0", " "),
                pack_cards="\n".join(pack_card(p, partials) for p in packs),
                footer_packs="\n".join(f'          <li><a href="{p["slug"]}.html">{esc(p["name"])}</a></li>' for p in packs),
                footer_faqs="\n".join(f'          <li><a href="{p["slug"]}.html#faq">{esc(p["faq_label"])}</a></li>' for p in packs),
                faq_buttons="\n".join(f'        <a class="btn btn-ghost" href="{p["slug"]}.html#faq">{esc(p["faq_label"])}</a>' for p in packs),
                faq_links=and_list([f'<a href="{p["slug"]}.html#faq">{esc(p["short_name"])}</a>' for p in packs]))
    for name, meta, tpl in pages:
        ctx = dict(base, **meta)
        ctx["noindex"] = bool(meta.get("noindex")) or draft
        ctx["base_tag"] = f'<base href="{html.escape(site_url, quote=True)}">\n' if (meta.get("is_404") and site_url) else ""
        current = ' aria-current="page"'
        ctx["nav_packs"] = "\n".join(
            f'        <li><a href="{p["slug"]}.html"{current if meta.get("nav_slug") == p["slug"] else ""}>{esc(p["nav_label"])}</a></li>'
            for p in packs)
        source = tpl if tpl is not None else open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        try:
            page = render(source, ctx, partials)
        except KeyError as e:
            sys.exit(f"{name}: {e.args[0]}")
        left = re.findall(r"\{\{[^}]*\}\}", page)
        if left:
            sys.exit(f"{name}: unresolved template tags {left[:3]}")
        open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(page)

    manifest = dict(name=base["publisher"], short_name="Sug's LowPoly", start_url="./", display="browser", background_color="#0b161e", theme_color="#0b161e",
                    icons=[dict(src="icon-512.png", sizes="512x512", type="image/png"), dict(src="apple-touch-icon.png", sizes="180x180", type="image/png")])
    json.dump(manifest, open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8", newline="\n"), indent=1)
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
        urls = "".join(f"  <url><loc>{html.escape(site_url + m['canonical_path'])}</loc><lastmod>{today}</lastmod></url>\n" for n, m, _ in pages if not m.get("noindex"))
        open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")

    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print(f"built {len(pages)} pages -> {OUT}  ({size / 1e6:.1f} MB)")
    for p in packs:
        print(f"  {p['slug']}.html  " + (f"store link: {p['resolved_store_url']}" if p["resolved_store_url"] else "no store link yet (Coming soon)"))
    if draft:
        print("DRAFT BUILD: support_email is empty in site.json. The contact page shows a placeholder and search engines are told not to index. Do not publish this build.")
    if not site_url:
        print("note: site_url is empty, so canonical links, the social preview image and sitemap.xml were left out. Set it once you know the final address.")


if __name__ == "__main__":
    main()
