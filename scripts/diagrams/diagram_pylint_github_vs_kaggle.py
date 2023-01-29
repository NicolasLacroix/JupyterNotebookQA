import matplotlib.pyplot as plt

from scripts.diagrams.extractor import read_files


def round_off_rating(number):
    """
    Round a number to the closest half integer.
    """
    return round(number * 2) / 2


def get_pylint_score(directory: str, source: str):
    jsons = read_files(directory)
    scores = []
    for element in jsons:
        try:
            if source not in element['notebook']:
                continue
            element = element['metrics']['code_quality']['pylint_score']['score']
            if element > 0:
                # Exclude notebooks equal to 0. Not relevant and they break the scale.
                scores.append(round_off_rating(element))
        except (TypeError, KeyError):
            pass
    return scores


def plot_diagram(directory: str, title: str):
    pylint_scores_github = get_pylint_score(directory, "github")
    pylint_scores_kaggle = get_pylint_score(directory, "kaggle")

    occurrences_github = dict(sorted({element: pylint_scores_github.count(element) for element in pylint_scores_github}.items()))
    occurrences_kaggle = dict(sorted({element: pylint_scores_kaggle.count(element) for element in pylint_scores_kaggle}.items()))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    github_plot = ax.plot(occurrences_github.keys(), occurrences_github.values(), '.-', color='r')
    if occurrences_kaggle:
        kaggle_plot = ax.plot(occurrences_kaggle.keys(), occurrences_kaggle.values(), '.-', color='b')
    ax.legend(("GitHub", "Kaggle") if occurrences_kaggle else ("Github", ), fontsize="large")
    ax.set_xlabel('Pylint score')
    ax.set_ylabel('Number of notebooks')
    ax.set_title(title)

    plt.xlim(0)
    plt.ylim(0)

    plt.grid()
    ax.set_axisbelow(True)
    plt.savefig(f"diagram_pylint_{'github_vs_kaggle' if occurrences_kaggle else 'github'}_{title}.png")

    plt.show()

if __name__ == '__main__':
    plot_diagram("../../results/", "Score of notebooks")
