import glob
import json

import matplotlib.pyplot as plt


def plot_profile():
    results = list(glob.glob('results/**/*.json', recursive=True))
    for result in results:
        with open(result) as f:
            json_data = json.load(f)
            if 'profile' not in json_data:
                print(f"Skipping {result}...")
                continue
            profile = json_data['profile']
            plot = [p['cell_type'] for p in profile]
            plt.plot(range(len(plot)), plot)
    plt.legend(results)
    plt.grid(True, which='both')
    plt.show()
