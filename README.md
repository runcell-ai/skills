# RunCell public skills

Official public Skill sources maintained by RunCell. Each package lives under `skills/`; host presentation metadata lives under `adapters/`.

| Skill | Purpose |
| --- | --- |
| academic-visualization | Prepare and check publication figures. |
| runcell-table-audit | Audit CSV files for missing values and duplicate rows. |
| runcell-notebook-health | Inspect saved notebook errors and execution state without running cells. |

## Build and verify

Use a project Python environment with the dependencies in `pyproject.toml` installed.

```sh
python scripts/official_skill_release.py build --skill-id academic-visualization --version 1.0.0 --output-dir /tmp/skill-bundles
python scripts/official_skill_release.py verify --bundle /tmp/skill-bundles/academic-visualization-1.0.0.zip --release /tmp/skill-bundles/academic-visualization-1.0.0.release.json
```

Published versions are immutable. Change the version when content changes. A source commit does not publish a package or add it to the automatic delivery catalog.

## Existing static distribution

The existing download origin remains [runcell-official-skills.vercel.app](https://runcell-official-skills.vercel.app/catalog/runtime-skills.json). This source migration preserves the existing catalog and published ZIP bytes. It does not deploy new content or publish a client.

`catalog/runtime-skills.json` is the automatic delivery catalog. `catalog/runcell-official-skills.json` retains the separate content-metadata format. Only academic-visualization is currently listed in the migrated automatic catalog. The table-audit ZIP is retained but not added to that catalog; notebook-health has source only.

Run `python scripts/prepare_static.py` to verify the existing packages and prepare `.deploy/`. Deploy that directory to the existing Vercel project `runcell-official-skills` in team `kanaries` only as a separate release action. The project is not linked to Git pushes. Keep previous immutable files, verify new ZIPs before listing them, and verify catalog freshness after deployment. Do not deploy the repository root.

## Source maintenance

This repository replaces `runcell-ai/runcell-official-skills` for public source maintenance. The old repository and live download artifacts are retained for compatibility. Skill source files and copied artifacts retain their original bytes; see [migration records](docs/migration-2026-10-29.md).

Imported content and tooling retain Apache-2.0 licensing. See [NOTICE](NOTICE) and [the retained license](LICENSES/Apache-2.0.txt). The root MIT license applies to new repository material unless otherwise stated.
