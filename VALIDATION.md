# Primary-build validation

Checked 2026-09-13. This record covers artifact integrity and visual usability,
not dimensional validation, installation approval or airworthiness.

| Check | Result |
|---|---|
| Scope attempted | 36 entries |
| Individual manuals | 33: 32 new plus approved CTRL001 |
| Instruction pages | 77 |
| Index | 2 pages; all 36 entries, revision, page count and status |
| Status | 1 RELEASED / 32 REVIEW REQUIRED / 3 BLOCKED |
| Consolidated human review | 46 items, BH-REV-001 through BH-REV-046 |
| PDF dimensions | Every instruction page 792 × 540 points |
| Image resolution | Every instruction PNG 4400 × 3000, lossless |
| PDF / image agreement | All 77 embedded instruction images match the released PNG pixels exactly |
| PDF web copies | All 34 PDFs in docs/pdf match their pdf/ originals byte for byte |
| Step order / bookmarks | Consecutive steps and one bookmark per instruction page |
| Editable sources | All 33 assembly .blend files reopen with meshes and orthographic cameras |
| Website | 36 scope pages plus contents, review and photo-index pages |
| Local links | 1,040 relative links and anchors checked; none missing or outside site root |
| Largest individual PDF | Under 15 MB; no GitHub single-file limit issue |
| CTRL001 preservation | Original Blender, Python source, PNGs, manifest and both PDF copies unchanged from baseline 2f35eab |

All 79 PDF pages were rasterized with Poppler. A full page contact-sheet pass
checked layout, titles, hardware callouts, color cues, detail framing and page
order. Targeted rechecks covered the corrected camera views, fuel bay, inspection
ring, wing tip, seat hinge, bellcrank pivot and single lift strut per wing.
The website was viewed at desktop, 1024 × 768 tablet, and 390 × 844 phone sizes.
Contents and step navigation worked; the phone manual had no horizontal overflow
and its instruction images loaded. Full-size links retain the original PNGs.

The selective photo index contains 35 reference records and 28 unopened candidate
folders. It distinguishes real photos, thumbnail-only reviews, drawings and
unreviewed candidates. No gallery image was labeled as confirmed Companion by
the available folder metadata. Other-model views were used only for local
relationships consistent with the supplied Companion plans and applicable
factory diagrams. The lift-strut and bellcrank comparisons caused corrections
before publication. Photos supplied no dimensions or critical hardware identity.

Review-required pages remain limited to their supported operations. Missing
drilling templates, source conflicts, unidentified equipment, unresolved washer
stacks and final rigging remain in the human queue. Tailwheel/stinger installation,
complete final rigging, and a separate vertical-fin installation remain BLOCKED.
No installation PDFs were fabricated for those three entries.

Reproducible integrity checks: `python scripts/validate_batch.py --render`.
Editable-source check: `blender -b --python scripts/check_blends.py`.
The latter refreshes embedded source/specification text for new files and never
saves the approved CTRL001 file. Temporary rasterizations and logs stay in ignored
`work/validation/`; they are not release assets.
