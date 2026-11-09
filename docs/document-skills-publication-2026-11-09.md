# Word and PDF automatic delivery publication

The 2026-11-09 release adds `word-documents` and `pdf`, both at 1.0.0, to
`catalog/runtime-skills.json`. Each declares minimum client version 0.2.9
and required tool `shell_execute`, following the existing catalog contract.
These entries require a client that implements automatic official delivery;
they do not install Python libraries, office applications, or fonts.

## Verified immutable packages

| Skill | Bytes | SHA-256 |
| --- | --- | --- |
| word-documents | 7288 | `92a2b64832dc75423a38ddf40d7a84f73f9429d633fe025502f7a388eddf59f1` |
| pdf | 6411 | `2089da4f6dca9589662688d4d2090cfd637a4819918c0fc11ace36d99ddc1b57` |

Each ZIP includes its MIT license in `references/LICENSE.txt`. The three
previous packages are unchanged. All five public downloads were compared
byte-for-byte with local packages and checked against release sizes and
SHA-256 digests before adding the new catalog entries.

## Release sequence

1. Committed and pushed `feat(skills): add portable Word and PDF packages`
   (`ac57f06bed61fe9bd23971fedccbb8a57ef25e7e`).
2. Prepared `.deploy/` using `scripts/prepare_static.py`, which verifies every
   archive and manifest. Published only its public assets and hosting config
   to project `runcell-official-skills`, team `kanaries`.
3. Package staging deployment `dpl_3WBXN9qCQdmJpaWLBzoPSJn3BUXg` became Ready;
   the production alias exposed both new ZIPs while retaining the old catalog.
4. Verified the public ZIPs, then used the client's
   `official_skills_catalog.py` helper to add both entries with schema validation.

The authoring/rendering checks and their limits are recorded in
[the portability record](document-skills-portability.md). Publication and
post-deployment integration results are recorded below after verification.
