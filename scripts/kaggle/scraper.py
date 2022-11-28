import os

os.environ['KAGGLE_CONFIG_DIR'] = f"{os.getcwd()}/scripts/kaggle"
print(os.environ.get('KAGGLE_CONFIG_DIR'))

from kaggle.api.kaggle_api_extended import KaggleApi
import tomli_w

api = KaggleApi()
api.authenticate()

file1 = open('scripts/kaggle/notebooks.txt', 'r')
lines = file1.readlines()
baseUrl = "https://www.kaggle.com/code/"
for line in lines:
    path = "../../notebooks/kaggle/"+line.strip().replace('/','-')+"/"
    author = line.strip().split('/', 1)[0]
    fileName = line.strip().split('/',1)[1]
    api.kernels_pull(line.strip(), path=path)
    with open(f"{path+fileName}.toml", "wb") as f:
        # DATE NOT FOUND : https://github.com/Kaggle/kaggle-api#kernels
        tomli_w.dump({'title': fileName,'metadata': {'path': fileName+'.ipynb', 'source': baseUrl+line.strip(), 'author': author, 'date': 'TODO'}}, f)
