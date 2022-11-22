import json
from pathlib import Path
from typing import Any
from uuid import uuid1

import tomllib
from pylint.lint import Run

NOTEBOOK = "notebooks/github/notebook"


def filter_cells_by(
    data: dict[str, Any], filter_key: str, filter_value: str
) -> tuple[dict[str, Any]]:
    return tuple(n for n in data["cells"] if n[filter_key] == filter_value)


def get_code_cells(data: dict[str, Any]) -> tuple[dict[str, Any]]:
    return filter_cells_by(data, "cell_type", "code")


def get_markdown_cells(data: dict[str, Any]) -> tuple[dict[str, Any]]:
    return filter_cells_by(data, "cell_type", "markdown")


with open(f"{NOTEBOOK}.ipynb", encoding="utf-8") as f:
    notebook = json.load(f)

with open(f"{NOTEBOOK}.toml", mode="rb", encoding="utf-8") as f:
    notebook_metadata = tomllib.load(f)

print(f"========= Analysing {notebook_metadata['title']} =========\n")

print("Analysing notebook structure...")

code_cells = get_code_cells(notebook)
markdown_cells = get_markdown_cells(notebook)

print(f"Number of code cells: {len(code_cells)}")
print(f"Number of markdown cells: {len(markdown_cells)}")
# TODO: check !pip use for dependencies installation
print(f"Dependencies installation cell detected ? {'!pip ' in code_cells[0]['source']}")

print("Analysing code quality (pylint)")

Path("tmp/").mkdir(parents=True, exist_ok=True)
pylint_scores = []
for code_cell in code_cells:
    tmp_filename = f"tmp/code_cell_{uuid1()}.py.tmp"
    tmp_path = Path(tmp_filename)
    with open(tmp_filename, mode="w", encoding='utf-8') as f:
        f.writelines(code_cell["source"])
        run = Run([tmp_filename], do_exit=False)
        pylint_scores.append(run.linter.stats.global_note)
    tmp_path.unlink()

print("\nExporting results...", end="")

results = {
    "title": notebook_metadata["title"],
    "notebook": f"{NOTEBOOK}.ipynb",
    "metadata": f"{NOTEBOOK}.toml",
    "metrics": {
        "nb_code_cells": len(code_cells),
        "nb_markdown_cells": len(markdown_cells),
        "dependencies_installation_detected": "!pip " in code_cells[0]["source"],
        "code_quality": {
            "pylint_scores": pylint_scores,
        },
    },
}

with open(
    f"results/{notebook_metadata['metadata']['author']}_{notebook_metadata['title']}.json",
    mode="w",
    encoding="utf-8",
) as f:
    json.dump(results, f, indent=4)

print(json.dumps(results, indent=4))

print("\ndone")
