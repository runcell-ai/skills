# RunCell official skills contributor rules

- Keep every directory under `skills/` portable across Agent hosts. Do not add RunCell, Codex, OpenAI, ChatGPT, Jupyter, or VS Code UI assumptions to the portable core unless the skill itself genuinely requires that host.
- Put host-specific presentation metadata under `adapters/<host>/`, outside the portable skill directory.
- A skill directory contains only `SKILL.md` and directly useful `references/`, `assets/`, or `scripts/`. Do not add changelogs, installation guides, test reports, or design history inside a skill.
- Official bundle versions are immutable. Publish a new SemVer version for every content change.
- Run bundle hash, manifest, and archive validation before publishing a release.
