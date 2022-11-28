import os

os.environ['KAGGLE_CONFIG_DIR'] = f"{os.getcwd()}/scripts/kaggle"

from kaggle.api.kaggle_api_extended import KaggleApi
import tomli_w
import requests

import pprint


def top_notebook(config_file: str = 'scripts/kaggle/notebooks.txt'):
    api = KaggleApi()
    api.authenticate()
    notebooks = api.kernels_list(sort_by="voteCount", page_size=4)
    with open(config_file, 'w') as f:
        for i in notebooks:
            f.write(str(getattr(i, "ref"))+"\n")

def scrap(config_file: str = 'scripts/kaggle/notebooks.txt'):
    api = KaggleApi()
    api.authenticate()

    file1 = open(config_file, 'r')
    lines = file1.readlines()
    baseUrl = "https://www.kaggle.com/code/"
    for line in lines:
        path = "notebooks/kaggle/"+line.strip().replace('/','-')+"/"
        author = line.strip().split('/', 1)[0]
        fileName = line.strip().split('/',1)[1]
        print(f"Saving {line.strip()}...", end="")
        api.kernels_pull(line.strip(), path=path)
        print("done")
        with open(f"{path+fileName}.toml", "wb") as f:
            # DATE NOT FOUND : https://github.com/Kaggle/kaggle-api#kernels
            print(f"Saving {path+fileName}.toml...", end="")
            tomli_w.dump({'title': fileName,'metadata': {'path': fileName+'.ipynb', 'source': baseUrl+line.strip(), 'author': author, 'date': 'TODO'}}, f)
            print("done")


if __name__ == '__main__':
    top_notebook()
    print(os.environ.get('KAGGLE_CONFIG_DIR'))
    scrap()
