# Sug's LowPoly — publisher website

Source and published copy of the Sug's LowPoly website, an independent Unity Asset Store publisher of low-poly asset packs.

Live site: https://guauglop.github.io/SugsLowPoly/

## Layout

| Path | What it is |
|---|---|
| `docs/` | The built site. GitHub Pages publishes this folder (Settings → Pages → branch `main`, folder `/docs`) |
| `src/` | Pages, partials, styles, script, fonts and images the site is built from |
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
