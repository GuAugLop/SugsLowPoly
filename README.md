# Sug's LowPoly — publisher website

Source and published copy of the Sug's LowPoly website, an independent Unity Asset Store publisher of low-poly asset packs.

Live site: https://guauglop.github.io/SugsLowPoly/

## Layout

| Path | What it is |
|---|---|
| `docs/` | The built site. GitHub Pages publishes this folder (Settings → Pages → branch `main`, folder `/docs`) |
| `src/` | Pages, partials, styles, script, fonts and images the site is built from |
| `src/data/packs/` | One JSON file per pack: texts, categories, gallery, specs, FAQ, card and images |
| `src/templates/pack.html` | The template every pack page is rendered from |
| `site.json` | The values that change: support email, site address, Asset Store links |
| `build.py` | Renders `src/` into `docs/`. Python 3 only, no dependencies |
| `brand/` | Logo, favicon and the publisher profile picture |
| `LEIA-ME.md` | Maintenance guide, in Portuguese |

## Updating the site

```
python build.py
git add -A
git commit -m "Update site"
git push
```

While `support_email` is empty in `site.json` the build is a draft: the contact page shows a placeholder and every page asks search engines not to index it.

The site is fully static and self-hosted: no cookies, no analytics, no third-party requests. Fonts (Anton, Barlow, Barlow Condensed) are used under the SIL Open Font License; the licence texts are in `src/assets/fonts`.

## Packs

| Pack | Page | Data file | Store link in `site.json` |
|---|---|---|---|
| Low Poly Enemy Melee Weapons | `low-poly-enemy-melee-weapons.html` | `src/data/packs/low-poly-enemy-melee-weapons.json` | `store_urls.low-poly-enemy-melee-weapons` (the older `pack_store_url` still works for this pack) |
| Low Poly Enemy Encampment Props | `low-poly-enemy-encampment-props.html` | `src/data/packs/low-poly-enemy-encampment-props.json` | `store_urls.low-poly-enemy-encampment-props` |

While a pack's store link is empty, its page and its card say "Coming soon". Paste the link and rebuild to switch them to "Available" with a button to the store.

### Adding a pack

1. Copy one of the files in `src/data/packs/` to `src/data/packs/<slug>.json`. The file name must be the slug, which is also the page name (`<slug>.html`). Set `order` to place it among the others.
2. Fill in the texts. Fields ending in `_html`, the paragraph and checklist lists, the spec values and the FAQ answers are HTML; the other fields are plain text. `nav_label` is the short name in the header menu (keep it short so the menu fits at 761 px). `pairs_with` (optional) adds a "Pairs well with" section that shows another pack's card.
3. Put the images in `src/assets/img/<folder>/`: `gallery/NN-name.webp` (1800 x 1200) and `gallery/NN-name-thumb.webp` (720 x 480), WebP quality 82; `pack-card-1200.webp` (1200 x 800); `pack-banner-2000.webp` (2000 x 1050) and `pack-banner-1100.webp` (1100 x 578); `og-image.jpg` (1200 x 630). Point `images` in the data file at them.
4. The page banner comes from CSS, because the Content Security Policy blocks inline styles: add two rules like the `art-encampment` ones at the end of `src/assets/css/site.css` and put the class name in `images.banner_class`.
5. Add `"<slug>": ""` to `store_urls` in `site.json`, run `python build.py`, and review the home page copy ("Two packs so far"), which is written by hand.

The build adds the page, the home card, the header and footer links and the sitemap entry by itself, and stops with a message if an image named in the data file is missing.
