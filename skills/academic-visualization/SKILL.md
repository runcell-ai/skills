---
name: academic-visualization
description: Prepare and QA quantitative figures for academic papers, journal submissions, notebooks, and scientific reports using target-aware publication requirements. Use when a user asks for publication-ready, journal-ready, single- or double-column, paper, manuscript, PDF/EPS/SVG/TIFF, or academic figures, especially when sizing, typography, accessibility, export, resolution, legends, labels, spacing, clipping, heatmaps, panels, or maps need refinement.
---

# Academic Visualization

Apply publication constraints, not a plotting tutorial or one universal house style. Let the base model choose the scientifically appropriate chart and implementation.

## Resolve the target, then style

1. Resolve the target journal or venue, manuscript stage, figure type, intended column span, and required files. Current journal instructions and templates override every default.
2. When a venue is named, verify its current official guide. Use [references/publisher-requirements.md](references/publisher-requirements.md) only to orient the search; it is not a substitute for the journal's live instructions.
3. Read [references/publication-style.md](references/publication-style.md) and apply the cross-journal principles that fit the figure.
4. If the target is unknown, do not invent an exact compliance profile or claim journal compliance. Produce a provisional, editable, final-size-readable figure and state the assumptions that still need a venue decision.
5. For Matplotlib/Seaborn, [assets/publication.mplstyle](assets/publication.mplstyle) provides export-safe neutral settings. It intentionally sets no canvas size, font size, DPI, grid, spine, or palette. Keep delivered code self-contained; never leave a runtime dependency on an absolute skill path.
6. Render and inspect the actual requested artifact at its intended physical size. Revise only failed scientific, venue, accessibility, or legibility constraints.

Protect these invariants:

- preserve data meaning, uncertainty, units, ordering, and scale; never infer semantics from value range alone;
- size and typography are evaluated at final output size, using the target's rules rather than a universal point size;
- identifiers are legible, unambiguous, and do not cover evidence;
- color is accessible and is not the sole carrier of meaning;
- generated line art stays vector when the target accepts it; raster resolution follows figure type and venue, without artificial upsampling;
- fonts, symbols, and editable elements survive export as required;
- captions or legends define abbreviations, symbols, error bars, and sample sizes when scientifically necessary;
- the exact final artifact has no clipping, collision, unintended rasterization, or lost content.

Use `scripts/inspect_static_figure.py` only when exact dimensions, a target-specific DPI threshold, or unchanged pixels need deterministic confirmation. Do not claim publication-ready without a known target and an inspected final artifact.
