#!/usr/bin/env python3
"""Inspect saved notebook outputs without executing or rewriting the notebook."""

import argparse
import json
from pathlib import Path


def inspect(source: Path) -> dict:
    notebook = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(notebook, dict) or notebook.get("nbformat") != 4:
        raise ValueError("Expected a Jupyter notebook in format 4")
    cells = notebook.get("cells")
    if not isinstance(cells, list) or not all(isinstance(cell, dict) for cell in cells):
        raise ValueError("Notebook cells must be a list of objects")
    code = [(index, cell) for index, cell in enumerate(cells) if cell.get("cell_type") == "code"]
    errors = []
    output_count = 0
    for index, cell in code:
        outputs = cell.get("outputs", [])
        if not isinstance(outputs, list) or not all(isinstance(output, dict) for output in outputs):
            raise ValueError(f"Invalid outputs in cell {index}")
        output_count += len(outputs)
        for output in outputs:
            if output.get("output_type") == "error":
                errors.append({"cell": index, "name": output.get("ename", ""),
                               "message": output.get("evalue", "")})
    return {"method": "runcell-notebook-health-v1", "cells": len(cells),
            "code_cells": len(code),
            "markdown_cells": sum(cell.get("cell_type") == "markdown" for cell in cells),
            "output_records": output_count,
            "unexecuted_code_cells": [index for index, cell in code if cell.get("execution_count") is None],
            "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("input and output must be different files")
    text = json.dumps(inspect(args.input), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
