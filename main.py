from pathlib import Path
from typing import Optional

import typer

from scripts import analysis, analysis_plot
from scripts.kaggle import scraper as kaggle_scraper

app = typer.Typer()


@app.command()
def analyze(directory: Optional[str] = typer.Argument('notebooks/')):
    print(f"Running analysis in directory: {directory}")
    for n in Path(directory).glob('**/*.ipynb'):
        print(f"Running for {n}...", end="")
        result = analysis.run_analysis(notebook_name=n.with_name(n.stem), verbose=False)
        print("done" if result else "error")


@app.command()
def display_profile():
    analysis_plot.plot_profile()


@app.command()
def scrap_github(config_filepath: str = typer.Argument('scripts/kaggle/notebooks.txt')):
    print(f"Scrapping github using config: {config_filepath}")


@app.command()
def scrap_kaggle(config_filepath: str = typer.Argument('scripts/kaggle/notebooks.txt')):
    print(f"Scrapping kaggle using config: {config_filepath}")
    kaggle_scraper.list_top_notebook(config_filepath)
    kaggle_scraper.scrap(config_filepath)
    


if __name__ == "__main__":
    app()
