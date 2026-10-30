# General Publication Figure Principles

These are cross-journal decision rules, not a house style. The target journal's current instructions and template are authoritative.

## Requirement precedence

Use this order:

1. journal-specific author guide, template, and production request;
2. explicit user requirements;
3. publisher-wide guidance;
4. provisional assumptions, clearly labelled as provisional.

Distinguish initial review from final production. A review PDF may be accepted even when production later requires separate editable or high-resolution files.

## Scientific integrity

- Preserve supplied values, uncertainty, sample definitions, units, category order, and scale meaning.
- Do not infer a metric or unit from its numeric range. Values between 0 and 1 are not necessarily probabilities.
- Do not connect unordered categories merely to improve styling or enable endpoint labels.
- Define error bars, abbreviations, symbols, scale transformations, and scientifically relevant sample sizes in the figure or caption as the venue requires.
- Keep comparable panels comparable; do not change limits, normalization, color scales, or encodings in ways that distort comparison.
- Treat microscopy, gels, blots, maps, and other captured images as evidence: do not remove, fabricate, selectively enhance, or hide features.

## Final-size layout

- Choose width from the target template; make height content-driven within the venue limit.
- Lay out and inspect the figure at intended publication size, not only zoomed on screen.
- Use space efficiently, but do not enforce a universal axes-area percentage. Panels, long scientific labels, maps, and required annotations legitimately need different geometry.
- Choose direct labels, a legend, or caption definitions according to lookup cost and available space. No legend position is universally correct.
- Keep identifiers off data, uncertainty intervals, and important image regions. Preserve scientific meaning when abbreviating or wrapping labels.
- Put figure numbers, titles, and captions where the target journal requests them; many journals keep titles and captions outside the artwork, but this is not universal.

## Typography

- Use the target's finished-size font range. There is no universal 7 pt rule.
- Keep typeface and hierarchy consistent across related figures, using standard fonts when the venue specifies them.
- Preserve editable text or embed fonts when required. Do not outline text when the venue needs editability.
- Check mathematical symbols, Greek characters, subscripts, superscripts, and minus signs in the exported artifact.
- Use concise axis wording and include units only when supplied or established by the source.

## Accessibility

- Do not rely on color alone; reinforce meaning with position, label, shape, line style, fill, or another appropriate cue.
- Use palettes and contrast that remain distinguishable for common color-vision deficiencies and grayscale reproduction when relevant. Avoid rainbow scales and red/green dependence unless the target explicitly requires them and an accessible alternative is unavailable.
- Avoid colored text as the only key. Keep text/background contrast high and place text away from busy imagery.
- Supply alt text or a long description when the venue requests it; captions and alt text serve different purposes.

## Format and resolution

- Prefer editable vector output for generated charts and line art when accepted by the venue.
- For raster content, use the venue's requirement for the actual art type: photographs/halftones, combination art, and line art commonly have different thresholds.
- Never manufacture detail by upsampling a low-resolution source. The lowest-resolution embedded element limits the composite figure.
- Export only the formats the workflow needs. PDF/SVG/EPS, TIFF/PNG/JPEG, and editable source requirements vary by journal and stage.
- Keep delivered plotting code and assets self-contained; do not leave absolute dependencies on the skill directory.

## Figure-specific checks

- Heatmaps: maintain comparable color scales where comparison requires it; keep colorbars from making labels unreadable.
- Multi-panel figures: preserve panel order, alignment, readable panel labels, and enough gutter to separate panels.
- Maps: preserve intended extent and projection, avoid clipped geography, and keep keys away from important regions.
- Image panels: retain scale bars and document legitimate processing or assembly in the caption/methods.

## Final artifact acceptance

At the intended physical size, confirm:

- values and encodings match the source;
- required dimensions, file type, color mode, font handling, and art-type resolution are satisfied;
- text, symbols, marks, scale bars, and uncertainty intervals are legible;
- nothing is clipped, corrupted, unintentionally rasterized, or covered;
- accessibility does not depend on color alone;
- the caption and artwork together preserve all necessary scientific meaning.
