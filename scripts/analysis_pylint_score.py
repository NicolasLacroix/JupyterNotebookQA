import glob
import json
import numpy as np
import matplotlib.pyplot as plt

def plot_profile():
    results = list(glob.glob('../results/*.json', recursive=True))
    print(results)
    x = []
    y = []
    for result in results:
        with open(result) as f:
            json_data = json.load(f)
            if "metrics" in json_data:
                x.append(json_data['metrics']['code_quality']['pylint_score']['score'])
                y.append(json_data['metrics']['nb_code_cells'])
    ########################
    fig = plt.figure()
    ax = fig.add_subplot(111)
    sizes = np.random.uniform(15, 80, len(x))
    colors = np.random.uniform(15, 80, len(x))
    ax.set(xlim=(0, 10), xticks=np.arange(1, 10), ylim=(0, 100), yticks=np.arange(0, 100, 5))
    ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)
    ax.set_xlabel('score')
    ax.set_ylabel('nb_code_cells')
    plt.show()

plot_profile()