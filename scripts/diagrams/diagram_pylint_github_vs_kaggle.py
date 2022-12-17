import matplotlib.pyplot as plt

from extractor import read_files


def round_off_rating(number):
    """
    Round a number to the closest half integer.
    """
    return round(number * 2) / 2


def get_pylint_score(source: str):
    jsons = read_files("../../results/")
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


if __name__ == '__main__':
    pylint_scores_github = get_pylint_score("github")
    pylint_scores_kaggle = get_pylint_score("kaggle")

    occurrences_github = [(lambda element: pylint_scores_github.count(element))(element) for element in
                          pylint_scores_github]
    occurrences_kaggle = [(lambda element: pylint_scores_kaggle.count(element))(element) for element in
                          pylint_scores_kaggle]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    github_scatter = ax.scatter(pylint_scores_github, occurrences_github, color='r')
    kaggle_scatter = ax.scatter(pylint_scores_kaggle, occurrences_kaggle, color='b')
    ax.legend((github_scatter, kaggle_scatter), ("GitHub", "Kaggle"))
    ax.set_xlabel('Pylint score')
    ax.set_ylabel('Number of notebooks')
    ax.set_title('Score of notebooks')

    plt.xlim(0)
    plt.ylim(0)
    plt.show()
