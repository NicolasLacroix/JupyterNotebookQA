import matplotlib.pyplot as plt

from extractor import read_files


def round_off_rating(number):
    """
    Round a number to the closest half integer.
    """
    return round(number * 2) / 2


def get_pylint_score():
    jsons = read_files("../../results/")
    scores = []
    for element in jsons:
        try:
            element = element['metrics']['code_quality']['pylint_score']['score']
            if element > 0:
                # Exclude notebooks equal to 0. Not relevant and they break the scale.
                scores.append(round_off_rating(element))
        except (TypeError, KeyError):
            pass
    return scores


if __name__ == '__main__':
    pylint_scores = get_pylint_score()

    occurrences = dict(sorted({element: pylint_scores.count(element) for element in pylint_scores}.items()))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(occurrences.keys(), occurrences.values(), '.-', color='r')
    ax.set_xlabel('Pylint score')
    ax.set_ylabel('Number of notebooks')
    ax.set_title('Score of notebooks')

    plt.xlim(0)
    plt.ylim(0)

    plt.grid()
    ax.set_axisbelow(True)

    plt.show()
