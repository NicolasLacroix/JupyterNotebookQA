import json
import tomllib
from typing import Any

NOTEBOOK = "notebooks/github/notebook"

def filter_cells_by(data: dict[str, Any], filter_key: str, filter_value: str) -> tuple[dict[str, Any]]:
    return tuple(n for n in data['cells'] if n[filter_key] == filter_value)

def get_code_cells(data: dict[str, Any]) -> tuple[dict[str, Any]]:
    return filter_cells_by(data, 'cell_type', 'code')

def get_markdown_cells(data: dict[str, Any]) -> tuple[dict[str, Any]]:
    return filter_cells_by(data, 'cell_type', 'markdown')

with open(f"{NOTEBOOK}.ipynb") as f:
    notebook = json.load(f)

with open(f"{NOTEBOOK}.toml", "rb") as f:
    notebook_metadata = tomllib.load(f)

print(f"========= Analysing {notebook_metadata['title']} =========\n")

code_cells = get_code_cells(notebook)
markdown_cells = get_markdown_cells(notebook)

print(f"Number of code cells: {len(code_cells)}")
print(f"Number of markdown cells: {len(markdown_cells)}")
# TODO: check !pip use for dependencies installation
print(f"Dependencies installation cell detected ? {'!pip ' in code_cells[0]['source']}")

print("\nExporting results...", end='')

results = {
    'title': notebook_metadata['title'],
    'notebook': f'{NOTEBOOK}.ipynb',
    'metadata': f'{NOTEBOOK}.toml',
    'metrics': {
        'nb_code_cells': len(code_cells),
        'nb_markdown_cells': len(markdown_cells),
        'dependencies_installation_detected': '!pip ' in code_cells[0]['source'],
    }
}

with open(f"results/{notebook_metadata['metadata']['author']}_{notebook_metadata['title']}.json", "w") as f:
    json.dump(results, f,  indent=4)

print("done")
