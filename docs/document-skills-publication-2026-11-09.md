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

5. Committed and pushed `feat(skills): publish Word and PDF to automatic catalog`
   (`1602b4f5b275f3b34f4c32fb021a23ec41dbef9c`). Catalog deployment
   `dpl_2YCcaqJr8RFPsz3EL1CEjr77Jvri` reached Ready and assigned the production
   alias without errors.

## Public and runtime verification

The production [catalog](https://runcell-official-skills.vercel.app/catalog/runtime-skills.json)
returned HTTP 200 and matched the committed catalog exactly, including all five
packages. Its response retained `Cache-Control: public, max-age=0, must-revalidate`
and `CDN-Cache-Control: no-store`, with cache age 0. No cache-busting query was
needed. Package downloads used their normal immutable URLs.

The real `OfficialDelivery` class from the RunCell client source was exercised
against this public HTTPS origin in an isolated temporary home. No mocks,
alternate catalog URLs, fabricated responses, or modified runtime limits were
used. The same Python process remained alive across catalog publication:

| Check | Elapsed | Result |
| --- | --- | --- |
| Initial sync before publication | 2.757 s | Three existing packages installed, no diagnostics |
| First sync after publication | 3.372 s | Both new packages installed, no diagnostics |

The second sync used the client's normal cached-catalog revalidation path and
five-second budget. Installed hashes matched the table above, both entrypoints,
helper scripts and licenses were present, and existing package hashes remained
unchanged. User configuration was isolated rather than modifying the user's
actual installation. The process exited successfully.

This verifies public distribution and the actual downloader/installer, not a
new full Jupyter or desktop UI task. Automatic delivery support and declared
tool availability are still required in the user's client. Installed skills
provide instructions and helper scripts; Python packages and native rendering
tools must be available separately.

The authoring/rendering checks and their limits are recorded in
[the portability record](document-skills-portability.md). The complete local
test suite passed with **8 tests**, with real file/render checks and no skips.
