# Agent instructions — michaelsieler.com

Sphinx Book Theme personal site (`.rst` sources, Read the Docs). Match existing page patterns; do not invent a parallel layout.

Do not edit `Archive/`, `_build/`, or `.venv`.

## Git

After every **major task** (a finished user request ready for the live site, not mid-exploration), commit and `git push` to the current branch (`master`).

- Short, sentence-case, why-focused commit messages
- Do not commit `_build/`, `.venv`, `.env`, Office lockfiles, or secrets
- Do not force-push

## Page template

Every content page except the homepage:

```rst
.. _Top:


Page Title
==========

...content...

------

Return to `top`_.

------
```

Heading marks (underline length must be ≥ title length):

- Homepage only (`index.rst`): `#` with overline + underline
- Page title: `=`
- Sections: `-`
- Subsections: `"`

## Visual system

Palette (ColorBrewer only; do not add colors, fonts, or themes):

- Green `#1b9e77` — external links
- Orange `#d95f02` — current/hover/active links, announcement banner
- Purple `#7570b3`
- Pink `#e7298a`
- Lime `#66a61e`
- Internal links `#346BE0`

Theme: `sphinx_book_theme`, light mode, logo-only header. Shared styles live in `_static/css/custom.css`.

## Images and media

Always include `:alt:`.

| Context | Directive | Size | Notes |
|---|---|---|---|
| Portraits / section photos | `.. image::` or `.. figure::` | `:align: center`, `:width: 30%` | |
| Schematic figures | `.. figure::` | `:align: center`, `:width: 50%` | |
| Poster detail pages | `.. image::` | `:align: center`, `:width: 90%` | `:target:` the image itself (not a hardcoded michaelsieler.com URL). Caption: `Click on poster to enlarge.` plus `:download:` when a PDF exists |
| Project GIFs / demos | `.. image::` | `:height: 300px` | |
| YouTube | `.. raw:: html` | `.video-container` wrapper | |
| Local `<video>` | `.. raw:: html` | `.media-block` class | No inline `style=` |

Swiper carousels: put only slide markup in RST. CSS/JS are global (`custom.css`, `_static/js/swiper-init.js`). Do not copy-paste Swiper `<style>`, `<link>`, or `<script>` into pages.

## Lists, tables, names

- Body bullets: `-` (not `*`)
- CV / dated entries: `.. list-table::` with `:widths: 80 20`
- Publications: `.. list-table::` with `:widths: 90 10`
- Career/Services skills: ASCII grid tables with hyphen bullets
- Own name in citation/CV rows: `**Michael J. Sieler Jr.**`

## Links and downloads

- Internal site links: relative paths (`Publications/publications.html`, `../Experience/experience.html`), not `https://michaelsieler.com/en/latest/...`
- Email: `mailto:Michael.SielerJr@UniGe.ch`
- `:download:` for PDFs — CSS already adds the download icon; do not also prefix `:icon:`fas fa-download``
- `:icon:`fas fa-download`` only on HTML poster-page links in `Publications/publications.rst`
- Resume section heading: `Download Resume & CV`

## Page-type notes

- **Experience:** list-tables, dated right column, resume downloads at the bottom
- **Publications:** citation list-tables; Swiper at top; poster rows link to `Publications/Presentations/` pages. Peer-reviewed and preprint rows are filled by `scripts/sync_openalex_publications.py` between `OPENALEX` markers; in-prep, talks, and Other stay manual. Do not hand-edit the marked blocks.
- **OpenAlex stub:** `Publications/openalex.rst` is an orphan redirect to the live Publications page; do not add it to the homepage toctree.
- **Projects:** `:height: 300px` media; Swiper for multi-image sets; "Tools used:" hyphen lists
- **Presentations:** poster template above (90% image, click-to-enlarge, optional PDF)
- **Homepage:** unique `#` title, 30% photo, hidden toctrees — do not add Career/Services to the nav unless asked
