import os

os.environ['KAGGLE_CONFIG_DIR'] = f"{os.getcwd()}/scripts/kaggle"
print(os.environ.get('KAGGLE_CONFIG_DIR'))

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

file1 = open('scripts/kaggle/notebooks.txt', 'r')
lines = file1.readlines()
for line in lines:
    print("Line: {}".format(line.strip()))
    api.kernels_pull(line.strip(), path="notebooks/kaggle/" + line.strip()+"/")
