# Primary-build validation

Checked 2026-09-13. This record covers artifact integrity and visual usability,
not dimensional validation, installation approval or airworthiness.

| Check | Result |
|---|---|
| Scope attempted | 36 entries |
| Individual manuals | 33: 32 new plus approved CTRL001 |
| Instruction pages | 79; 81 total PDF pages including index |
| Index | 2 pages; all 36 entries, revision, page count and status |
| Status | 1 RELEASED / 32 REVIEW REQUIRED / 3 BLOCKED |
| Consolidated human review | 51 items; original BH-REV-001 through BH-REV-046 retained; five appended identifiers |
| PDF dimensions | Every instruction page 792 × 540 points |
| Image resolution | Every instruction PNG 4400 × 3000, lossless |
| PDF / image agreement | All 79 embedded instruction images match the published PNG pixels exactly |
| PDF web copies | All 34 PDFs in docs/pdf match their pdf/ originals byte for byte |
| Step order / bookmarks | Consecutive steps and one bookmark per instruction page |
| Editable sources | All 33 assembly .blend files reopen with meshes and orthographic cameras |
| Website | 40 pages: 36 scope pages plus contents, review, photo and Beartracks reference indexes |
| Local links | 1,161 relative links and anchors checked; none missing or outside site root |
| Largest individual PDF | Under 15 MB; no GitHub single-file limit issue |
| CTRL001 preservation | Original Blender, Python source, PNGs, manifest and both PDF copies unchanged from baseline 2f35eab |

The preceding primary-build edition's 79 PDF pages were rasterized with Poppler. A full page contact-sheet pass
checked layout, titles, hardware callouts, color cues, detail framing and page
order. Targeted rechecks covered the corrected camera views, fuel bay, inspection
ring, wing tip, seat hinge, bellcrank pivot and single lift strut per wing.
The website was viewed at desktop, 1024 × 768 tablet, and 390 × 844 phone sizes.
Contents and step navigation worked; the phone manual had no horizontal overflow
and its instruction images loaded. Full-size links retain the original PNGs.

The selective photo index now contains 39 reference records and 28 unopened candidate
folders. It distinguishes real photos, thumbnail-only reviews, drawings and
unreviewed candidates. No gallery image was labeled as confirmed Companion by
the available gallery-folder metadata. The new 2024 Beartracks walk-around
explicitly identifies Jay Townsend's Companion. Other-model views were used only for local
relationships consistent with the supplied Companion plans and applicable
factory diagrams. The lift-strut and bellcrank comparisons caused corrections
before publication. Photos supplied no dimensions or critical hardware identity.

## Beartracks update

Ten supplied PDFs (409 sheets) were screened for relevant primary-build material.
Selected articles and illustrations received full-page review; the scanned Patrol
compilation received a 63-sheet visual screening. The 32-entry selective reference
index records model applicability, page locations, adopted checks and excluded
historical specifications. Current manufacturer-hosted alerts were also read,
including all four AD-002 sheets and the AD-004, OA-001 and OA-002 sheets.

Nine manuals were revised to v3. All 24 pages in the changed PDFs (including the
two-page index) were freshly rasterized and visually checked for layout, callouts,
orientation and detail framing. New views cover loaded gear spread and outboard
trim-arm joints; the flap view identifies aft-pulley inspection access. The gear
illustration was compared with Companion installation photography; trim and aft
pulley interpretations remain constrained by plans/factory diagrams where a
matching installation photograph was unavailable. No visual measurement was
promoted to a critical specification.

All 33 Blender files reopened with meshes and orthographic cameras. The nine
changed files embed the updated specification and source. Hash comparisons
confirmed the original CTRL001 assets and every unaffected PDF unchanged.
Original review identifiers retain their manual associations. The updated alert
links and manual step navigation were checked in the browser; reference and brake
pages also passed 390 x 844 phone checks without horizontal overflow, and both
brake instruction previews loaded.

The brake replacement/restrictor requirement and aft-flap-pulley service alert
are explicit. The newsletter/factory flap-speed conflict remains unresolved in
BH-REV-049. No review-required or blocked assembly was promoted by this update.

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
