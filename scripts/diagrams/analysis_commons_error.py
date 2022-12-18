from extractor import read_files


def get_error_stats():
    jsons = read_files("../../results/")
    error_stats = {}
    for element in jsons:
        try:
            pylint = element['metrics']['code_quality']['pylint_score']['score']
            if pylint == 0:
                # Exclude notebooks where pylint is equals to 0. Not relevant.
                continue

            errors = element['metrics']['code_quality']['pylint_score']['count_by_messages']
            for key, value in errors.items():
                if key not in error_stats:
                    error_stats[key] = value
                else:
                    error_stats[key] += value
        except (TypeError, KeyError):
            pass

    return dict(sorted(error_stats.items(), key=lambda item: item[1], reverse=True))


if __name__ == '__main__':
    stats = get_error_stats()
    print(stats)
