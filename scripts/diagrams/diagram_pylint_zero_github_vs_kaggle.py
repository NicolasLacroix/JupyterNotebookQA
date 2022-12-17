import matplotlib.pyplot as plt

from extractor import read_files


def get_pylint_score(zero: bool, source: str):
    jsons = read_files("../../results/")
    counter = 0
    for element in jsons:
        try:
            if source not in element['notebook']:
                continue
            element = element['metrics']['code_quality']['pylint_score']['score']

            if (zero and element == 0) or (not zero and element > 0):
                counter += 1
        except (TypeError, KeyError):
            pass
    return counter


if __name__ == '__main__':
    pylint_zero_github = get_pylint_score(True, "github")
    pylint_zero_kaggle = get_pylint_score(True, "kaggle")

    pylint_not_zero_github = get_pylint_score(False, "github")
    pylint_not_zero_kaggle = get_pylint_score(False, "kaggle")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    axis_x_legend_not_zero = "Pylint > 0"
    axis_x_legend_zero = "Pylint = 0"

    github_zero_bars = ax.bar("GitHub (PL = 0)", pylint_zero_github, 0.5, color='r')
    github_not_zero_bars = ax.bar("GitHub (PL > 0)", pylint_not_zero_github, 0.5, color='r')

    kaggle_zero_bars = ax.bar("Kaggle (PL = 0)", pylint_zero_kaggle, 0.5, color='b')
    kaggle__not_zero_bars = ax.bar("Kaggle (PL > 0)", pylint_not_zero_kaggle, 0.5, color='b')

    names_list = ["GitHub (PL = 0)", "GitHub (PL > 0)", "Kaggle (PL = 0)", "Kaggle (PL > 0)"]
    values_list = [pylint_zero_github, pylint_not_zero_github, pylint_zero_kaggle, pylint_not_zero_kaggle]
    for i, (name, height) in enumerate(zip(names_list, values_list)):
        ax.text(i, height-5, ' ' + str(values_list[i]), color='seashell',
                ha='center', va='top', rotation=0, fontsize=18)

    ax.set_title('Pylint of notebooks')

    plt.show()
