# bearhawk-companion-build-guide
Bearhawk Companion Build Guide

Primary-build visual guide, following the approved CTRL001 v2 style.

- [Open the guide](docs/index.html)
- [Open the Photo Library](docs/photos/index.html)
- [Photo Library import and maintenance guide](PHOTO_LIBRARY.md)
- [Download the manual index](pdf/00_Manual_Index.pdf)
- [Human review queue](HUMAN_REVIEW_REQUIRED.md)
- [Photo index](PHOTO_INDEX.md)
- [Beartracks and factory reference index](BEARTRACKS_INDEX.md)
- [Validation record](VALIDATION.md)
- [Git publication status](GIT_STATUS.md)

33 individual manuals (32 new plus preserved CTRL001), 79 instruction pages,
a 2-page index, and 36 scope pages. Status: 1 RELEASED, 32 REVIEW REQUIRED,
3 BLOCKED. There are 51 consolidated review items.

The Beartracks update revises nine manuals to v3, adding gear-spread and
trim-arm checks, current factory brake/flap alerts and hinge/rigging references.
Existing `_v2` asset filenames remain stable URLs; the catalog, page footer and
manual index show the actual revision. Original review identifiers are preserved.

The PDFs in `pdf/` and `docs/pdf/` are identical copies. Each manual has its
own web page and editable Blender file. The three blocked operations have
web pages identifying the missing information, without an invented PDF.

Plans control design. The current Companion hardware count sheet controls
explicit quick-build hardware. Photos supply appearance and orientation only.
Review-required illustrations communicate supported relationships; they do not
release unresolved drilling, washer stacks, cable lengths, torque or rigging.
The label RELEASED is limited to the illustrated operation and is not an
airworthiness determination. Avionics and firewall-forward work are excluded.

## Rebuild one manual

Requirements: Blender 5.2 LTS, Python 3, Pillow, ReportLab, pypdf, and Arial
regular/bold fonts. `BH_FONT_DIR` can point to a font directory containing
`arial.ttf` and `arialbd.ttf`. Poppler's `pdftoppm` supports visual PDF checks.

```text
python scripts/build_catalog.py
python scripts/primary_visuals.py --ids WING003 --blender "path/to/blender"
python scripts/publish_all.py --ids WING003
python scripts/validate_batch.py --render
```

Omit `--ids` to rebuild all new manuals. CTRL001 is preserved by the bulk
pipeline; its original source remains `scripts/ctrl001_visual_v2.py`.
`--compose-only` rebuilds page graphics from the local render cache.
`python scripts/publish_all.py --web-only` updates web pages and review indexes.
`python scripts/reference_index.py` reproduces the selective photo index.
Run `blender -b --python scripts/hardware_icons.py` if hardware shape icons change.

Catalog and source decisions are in `specs/`. The `.blend` files embed their
source and assembly specification. New assembly files contain a scene for each
step and main/detail orthographic cameras. Geometry is illustrative, not a
manufacturing model. Temporary render caches and extracted source PDFs stay in
ignored `work/`; the supplied original manuals and gallery images are not
redistributed in this repository.

## Website publication

The existing GitHub Actions workflow publishes `docs/` on a push to `main`.
GitHub Pages must use GitHub Actions as its deployment source. All local links
are relative, so the site works at the repository URL prefix as well as locally.
The website uses lightweight previews with links to full-resolution PNGs.
No external service or JavaScript is required to read the guide. The Photo
Library uses optional JavaScript for search, filters and the larger viewer;
category and individual-photo pages also work without it.
