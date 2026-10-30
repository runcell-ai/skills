# Runtime catalog publication, 2026-10-30

The automatic delivery catalog now lists the three existing public Skills below. The immutable ZIPs were staged before the new catalog entries. No client was published by these deployments. Independent real-client acceptance passed on Jupyter and macOS Desktop. Each client installed both new IDs on its first task after publication. The first client release containing automatic delivery has not been published.

## Immutable packages

| Skill | Version | Bytes | SHA-256 |
| --- | --- | --- | --- |
| academic-visualization | 1.0.0 | 8414 | `0f2877448b103e5b7f88129cf3694cc81e98992d0d441dba7365f585d65eb352` |
| runcell-table-audit | 1.0.0 | 2369 | `dd392300e3a8dac4d17de9d2e89ac26d353e12ec53d3855fbf7f03423cea032a` |
| runcell-notebook-health | 1.0.0 | 2246 | `5941889fcf81a9e7250a5321cae423e51cab896a9821a1966090bdf98e9ee179` |

Package URLs use `https://runcell-official-skills.vercel.app/packages/<skill>-1.0.0.zip`. The catalog is [catalog/runtime-skills.json](https://runcell-official-skills.vercel.app/catalog/runtime-skills.json).

All three entries require client version `0.2.9` or newer. Table audit and notebook health also declare `shell_execute`. These requirements do not supply tools or bypass their permissions. A client must contain the automatic delivery implementation to fetch this catalog; a version number alone does not establish that support.

## Publication records

Deployment IDs and Ready times below come from the deployment receipts. All times are UTC. These are content deployments to Vercel project `runcell-official-skills` in team `kanaries`.

| Date | Source commit | Deployment | Ready at |
| --- | --- | --- | --- |
| 2026-10-30 | [feat(skills): package notebook health for official delivery](https://github.com/runcell-ai/skills/commit/506c896a61feb460aabe259e0f1286a8de360052) | `dpl_HEDGSa8XiDdYFXintZkEqys7Db3C` | 2026-10-30T09:49:55.171Z |
| 2026-10-30 | [feat(skills): publish table audit to automatic catalog](https://github.com/runcell-ai/skills/commit/21769c854bc3e82925d15dbc9164cb5b9968bd45) | `dpl_Ah38RZNMRTbemJn8YJoNMELQEdUb` | 2026-10-30T09:57:26.400Z |
| 2026-10-30 | [feat(skills): publish notebook health to automatic catalog](https://github.com/runcell-ai/skills/commit/d35eb57f439976b7a1697ca7e11a88f96e7232ac) | `dpl_9NjeanVn1j72whLKwZVZokfjycH3` | 2026-10-30T09:59:53.727Z |

The first deployment staged notebook-health's ZIP while retaining the academic-only catalog. The next deployment added table-audit, and the last added notebook-health. Academic's existing package bytes remained unchanged throughout. The 2026-10-29 migration record describes the repository state at migration time and is retained as history.

Before the two new catalog entries, one HTTPS GET per package verified the public table-audit and notebook-health ZIPs against their release metadata and local ZIP bytes. Both returned HTTP 200 with the sizes and digests above. This package check verifies downloads; the complete client checks separately covered cold installation, both new-ID publications, lazy reads and read-only management. Bad-network retries were also recorded; this is not a guarantee that every task can download a new package within the five-second preparation budget.

## Maintaining publications

Git pushes do not deploy this site. Prepare the static output with `scripts/prepare_static.py` and deploy `.deploy/` separately. Verify immutable public ZIP bytes before publishing their catalog entries, and keep earlier immutable packages available. Never deploy the repository root or private source repository.

The initial delivery implementation added compatible new IDs only. [The same-ID update follow-up](https://github.com/ObservedObserver/d5m/pull/270) extends the same check before a new Agent task to install compatible, strictly higher versions. Existing tasks keep their original official versions, and failed updates retain the old installation. Same-version content changes and lower versions are ignored; removing an entry does not uninstall it. Clients without this implementation retain their existing Skills behavior until upgraded. This follow-up does not change the three 1.0.0 publications recorded above or publish a client.
