---
name: runcell-notebook-health
description: Inspect a saved Jupyter notebook for execution errors, unexecuted code, cell counts and output counts, then save a notebook health report without executing cells.
---

Read `references/reporting.md`. Run `scripts/inspect_notebook.py` from this
package with the saved notebook path and destination JSON path, using the
workspace's Python interpreter. The script needs only the standard library.

```sh
python /path/to/this/skill/scripts/inspect_notebook.py analysis.ipynb health.json
```

Use the runtime's task copy when supplied. Inspect the saved report. Do not
execute cells, open a kernel, or rewrite the notebook for this inspection.
