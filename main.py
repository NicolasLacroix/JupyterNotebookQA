from pathlib import Path
from typing import Optional

import typer

from scripts import analysis

app = typer.Typer()


@app.command()
def analyze(directory: Optional[str] = typer.Argument('notebooks/')):
    print(f"Running analysis in directory: {directory}")
    for n in Path(directory).glob('**/*.ipynb'):
        print(f"Running for {n}...", end="")
        result = analysis.run_analysis(notebook_name=n.with_name(n.stem), verbose=False)
        print("done" if result else "error")


@app.command()
def scrap_github(config_filepath: str):
    print(f"Scrapping github using config: {config_filepath}")


@app.command()
def scrap_kaggle(config_filepath: str):
    print(f"Scrapping kaggle using config: {config_filepath}")


if __name__ == "__main__":
    app()
