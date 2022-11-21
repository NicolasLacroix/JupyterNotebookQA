from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

file1 = open('notebooks.txt', 'r')
lines = file1.readlines()
for line in lines:
    print("Line: {}".format(line.strip()))
    api.kernels_pull(line.strip(), path="../../notebooks/kaggle/" + line.strip()+"/")
