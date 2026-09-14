# Photo Library

The existing site now includes `/photos/`: 19 curated local photo examples,
67 component categories, 47 indexed sources, source-aware captions and a
separate import review queue. Categories without reviewed photos say so.
The 39 previous reference records remain at `/photos/reference-index/`;
their old `/photos/#ID` bookmarks remain usable.

## What changed

- `specs/photo-library/`: photo metadata, JSON Schema, taxonomy, source directory
  and public review summaries. Metadata is independent of page presentation.
- `scripts/photo_library.py`: category pages, photo pages, source/review pages,
  guide links and metadata validation.
- `docs/assets/css/photo-library.css` and `docs/assets/js/photo-library.js`:
  responsive cards, full-text search, eight filters, sort, pagination and an
  accessible native-dialog viewer with related photos, keyboard controls and
  shareable links. Individual photo pages work without JavaScript.
- `scripts/import_photos.py`: local directory/HTML and PDF import staging,
  duplicate detection, provenance preservation and explicit reviewed publishing.
- `scripts/publish_all.py` and shared CSS: primary navigation and links from
  existing guides. All instruction PDFs, PNGs and Blender scenes are preserved.

## Sources and interpretation

Two seed images explicitly identify Jay Townsend's Companion in the supplied
2024 Beartracks walk-around. Seventeen selected factory/legacy-manual images
have unidentified photo models; they are deliberately labeled Unknown, including
images from manuals applicable to more than one model. A manual's applicability
does not prove the aircraft pictured is a Companion. The initial curated records
record Codex's visual/source review, not a fictional human sign-off.

Original embedded image bytes are retained beside optimized WebP previews.
Small source images are not upscaled or advertised as high-resolution originals.
PDF names, one-based PDF pages, printed pages where known, embedded image names,
hashes and attribution remain in metadata. An embedded PDF image name is not
claimed to be the original camera filename. Source captions are transcribed only
where their association is clear; other captions remain available in the source.

External sources are link-only in this first pass. The directory distinguishes
verified author/model context, previously indexed galleries, inaccessible pages
and the CD that has not yet arrived. No credentials, complete newsletters,
commercial manuals or mirrored external photo collections are published.
The initial selected local images follow the owner's project brief; this does
not assert a general license to redistribute those source collections.

The source page records the requested eight-level authority hierarchy and seven
conclusion classifications. Photos supply orientation, access and visual
relationships; they never establish critical specifications. Updated hardware
workbooks are separately indexed with hashes; filenames do not automatically
supersede the existing Companion hardware callouts.

## Rebuild

Use the project's existing Python environment (Python 3, Pillow, pypdf and
ReportLab). No database, front-end framework, service account or new package is
required.

```sh
python scripts/publish_all.py --web-only
python scripts/test_photo_library.py
python -m http.server 8766 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:8766/photos/`. GitHub Pages also supports the repository
prefix: `/bearhawk-companion-build-guide/photos/`.

## Import a local directory or the future Russ Erb CD

Copy/read the CD locally, then stage it outside `docs/`. Choose a new batch
directory each time. The importer does not execute HTML, follow web links or
download remote resources.

```sh
python scripts/import_photos.py directory "path/to/CD" --out work/imports/erb-001 --source-name "Russ Erb Bearhawk CD" --source-type "Builder Manual" --builder "Russ Erb" --source-url "http://bhcd.erbman.org/"
```

The batch preserves image files and HTML indexes under `originals/`, maintaining
their directory structure. `manifest.json` holds the image records, original
paths, hashes and HTML-image caption associations. `context.json` preserves
HTML text and links for review. Exact duplicate images are flagged. Similar
views still need editorial selection; no automated model/component guessing is
performed. Every imported record starts `pending` and model `Unknown`.

## Extract selected PDF pages

```sh
python scripts/import_photos.py pdf "path/to/manual.pdf" --pages 17,18,19 --out work/imports/manual-001 --source-name "Legacy fuselage manual" --source-type "Bearhawk Factory"
```

Omit `--pages` to process all PDF pages. Small embedded images below 100 pixels
on either axis are skipped by default (`--min-size` changes that threshold).
Page text stays in local `context.json`; image provenance includes PDF filename,
page and embedded image name. Logos, diagrams, duplicates and ambiguous images
must be removed or rejected during review. Scanned whole-page images require
manual selection; this importer does not guess photograph boundaries.

## Human review and publication

1. Inspect each staged image with its source text. Fill the component/category,
   useful description, builder/model evidence, applicability and attribution.
2. Use the vocabulary in `taxonomy.json` and `photo.schema.json`. Leave unknown
   facts explicitly Unknown; do not promote a guess into a model label or hardware
   requirement. Record the unresolved issue in `applicabilityNotes`.
3. Record image-use rights in `rightsBasis` and `copyrightNotes`. For an external
   source without appropriate permission, retain only its entry in `sources.json`.
4. A human reviewer sets `reviewStatus` to `approved`, records their actual name
   in `humanReviewer`, and fills `reviewedAt`, `reviewNotes` and `evidence`.
   `curated` is reserved for the initial, owner-requested seed and is not accepted
   by the batch publisher. Pending/rejected records and exact duplicates are skipped.
5. Add concise public review summaries to `review-queue.json` where useful. Do not
   include private staged images, full article text or credentials there.
6. Publish only reviewed records, rebuild, test, inspect the result and commit:

```sh
python scripts/import_photos.py publish-reviewed work/imports/erb-001
python scripts/publish_all.py --web-only
python scripts/test_photo_library.py
```

This is an editorial file workflow, not an authentication system. The command
does not invent approval or contact a reviewer. Check original images for private
EXIF metadata before approving them for public hosting. Preserve provenance while
removing private data only when authorized. Keep staged batches inside ignored
`work/` and never commit credentials or whole commercial reference collections.

## Validation

The focused suite covers schema/model checks, human-review and rights gates,
directory traversal rejection, preserved HTML captions/paths, duplicate detection,
an approved import round trip, all local site links and old reference bookmarks.
It also compares build-artifact hashes when the local session baseline is present.
The initial implementation was inspected at desktop and 390 × 844 phone sizes.
Search, model/combined filters, empty states, keyboard closing, focus restoration,
original-image links, category routes and existing-guide navigation were checked.

New categories can be added to `taxonomy.json`. Subsystem and component routes
are generated from that hierarchy. The gallery renders 24 results at a time,
uses lazy thumbnails and searches local metadata. Very large imports may warrant
splitting the metadata index by category; the data model and provenance remain
unchanged.
