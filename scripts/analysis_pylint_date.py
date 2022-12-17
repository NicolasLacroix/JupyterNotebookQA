import glob
import json
import tomllib
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def plot_profile(source: str):
    elems = dict()
    toml_files = list(glob.glob(('../notebooks/' + source + '/*/*.toml'), recursive=True))
    for toml_file in toml_files:
        with open(toml_file, "rb") as f2:
            data = tomllib.load(f2)
            if source == 'github':
                convert_date = datetime.strptime(data['metadata']['date'], '%d/%m/%Y').date()
            else:
                convert_date = datetime.strptime(data['metadata']['date'], '%Y-%m-%d').date()

            elems[data['title']] = convert_date
    print(len(elems))
    json_results = list(glob.glob('../results/*.json', recursive=True))
    x = []
    y = []
    for key, val in elems.items():
        res = [i for i in json_results if key in i]
        if len(res) > 0:
            with open(res[0]) as f:
                json_data = json.load(f)
                if "metrics" in json_data and json_data['metrics']['code_quality']['pylint_score']['score'] > 0:
                    x.append(val)
                    y.append(json_data['metrics']['code_quality']['pylint_score']['score'])
    print(len(y))
    return x, y


github_result = plot_profile('github')
kaggle_result = plot_profile('kaggle')
fig, ax = plt.subplots()
ax.set(ylim=(0, 10), yticks=np.arange(1, 10))
github_scatter = ax.scatter(github_result[0], github_result[1], linewidth=2.0, c='red')
kaggle_scatter = ax.scatter(kaggle_result[0], kaggle_result[1], linewidth=2.0, c='blue')
ax.legend((github_scatter, kaggle_scatter), ("GitHub", "Kaggle"))
ax.set_xlabel('date')
ax.set_ylabel('score')
plt.xticks(rotation=70)
plt.show()
