import json
import tomllib

with open("notebooks/github/notebook.ipynb") as f:
    notebook = json.load(f)

with open("notebooks/github/notebook.toml", "rb") as f:
    notebook_metadata = tomllib.load(f)

print(f"========= Analysing {notebook_metadata['title']} =========\n")

print(f"Number of code cells: {len(tuple(n for n in notebook['cells'] if n['cell_type'] == 'code'))}")
print(f"Number of markdown cells: {len(tuple(n for n in notebook['cells'] if n['cell_type'] == 'markdown'))}")
