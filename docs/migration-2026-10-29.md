# Source migration, 2026-10-29

Moved maintenance of academic-visualization, runcell-table-audit and runcell-notebook-health here. Existing catalog and immutable packages were copied without changes. The previously local OpenAI academic adapter is included.

File provenance and SHA-256 values are recorded in [the migration manifest](migration-files-2026-10-29.json). All Skill content bytes match their sources. Original Apache-2.0 license text is retained under LICENSES/.

Existing source copies and deployed artifacts were retained. This migration does not deploy the catalog, add automatically delivered IDs, publish a client, or certify the pending automatic-delivery acceptance.

Validation: all migrated Skill files passed the existing package collector and their recorded SHA-256 checks. The existing release-tool tests passed 3/3. The prepared static catalog, packages, release records and Apache LICENSE match the old source artifacts byte for byte. No deployment was performed.
