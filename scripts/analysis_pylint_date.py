import glob
import json
import tomllib
import numpy as np
import matplotlib.pyplot as plt

def plot_profile():

    elems = dict()
    toml_files = list(glob.glob(('../notebooks/*/*/*.toml'), recursive=True))
    for toml_file in toml_files:
        with open(toml_file, "rb") as f2:
            data = tomllib.load(f2)
            elems[data['metadata']['date']] = data['title']
    elems = dict(sorted(elems.items()))

    json_results = list(glob.glob('../results/*.json', recursive=True))
    x = []
    y = []
    for key, val in elems.items():
        res = [i for i in json_results if val in i]
        if len(res) > 0:
            with open(res[0]) as f:
                json_data = json.load(f)
                if "metrics" in json_data and json_data['metrics']['code_quality']['pylint_score']['score'] > 0:
                    x.append(key)
                    y.append(json_data['metrics']['code_quality']['pylint_score']['score'])
    ########################
    fig, ax = plt.subplots()
    ax.set(ylim=(0, 10), yticks=np.arange(1, 10))
    ax.plot(x, y, linewidth=2.0)
    ax.set_xlabel('date')
    ax.set_ylabel('score')
    plt.xticks(rotation=70)
    plt.show()

plot_profile().strip("\\")[1]