import matplotlib.pyplot as plt

from extractor import read_files


def get_cells_stats(source: str):
    jsons = read_files("../../results/")
    cells_stats = []
    for element in jsons:
        try:
            if source not in element['notebook']:
                continue
            pylint = element['metrics']['code_quality']['pylint_score']['score']
            code = element['metrics']['nb_code_cells']
            markdown = element['metrics']['nb_markdown_cells']
            if pylint > 0:
                # Exclude notebooks where pylint is equals to 0. Not relevant.
                cells_stats.append({"code": code, "markdown": markdown})
        except (TypeError, KeyError):
            pass
    return cells_stats


if __name__ == '__main__':
    cells_stats_github = get_cells_stats("github")
    cells_stats_kaggle = get_cells_stats("kaggle")

    code_github = [element['code'] for element in cells_stats_github]
    code_kaggle = [element['code'] for element in cells_stats_kaggle]

    markdown_github = [element['markdown'] for element in cells_stats_github]
    markdown_kaggle = [element['markdown'] for element in cells_stats_kaggle]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    github_scatter = ax.scatter(code_github, markdown_github, color='r')
    kaggle_scatter = ax.scatter(code_kaggle, markdown_kaggle, color='b')
    ax.legend(("GitHub", "Kaggle"))
    ax.set_xlabel('Cells of code')
    ax.set_ylabel('Cells of markdown')
    ax.set_title('Cells of code and markdown')

    plt.xticks(range(0, 250, 25))
    plt.yticks(range(0, 250, 25))
    plt.grid()
    ax.set_axisbelow(True)

    plt.xlim(0)
    plt.ylim(0)
    plt.show()
