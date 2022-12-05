import glob
import json

import matplotlib.pyplot as plt


def plot_profile():
    results = list(glob.glob('results/**/*.json', recursive=True))
    for result in results:
        with open(result) as f:
            profile = json.load(f)['profile']
            plot = [p['cell_type'] for p in profile]
            plt.plot(range(len(plot)), plot)
    plt.legend(results)
    plt.grid(True, which='both')
    plt.show()
