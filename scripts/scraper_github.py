import io
import os
import shutil
import zipfile

import requests
from requests import Response

tmp_directory_suffix = "-tmp"

repositories = [
    {"owner": "Pierian-Data", "repo": "Complete-Python-3-Bootcamp"}
    # {"owner": "trekhleb"},
    # {"owner": "norvig"},
    # {"owner": "MLEveryday"},
    # {"owner": "dennybritz"},
    # {"owner": "wesm"},
    # {"owner": "slundberg"},
    # {"owner": "zergtant"},
    # "https://github.com/trekhleb/homemade-machine-learning",
    # "https://github.com/norvig/pytudes",
    # "https://github.com/MLEveryday/100-Days-Of-ML-Code",
    # "https://github.com/dennybritz/reinforcement-learning",
    # "https://github.com/wesm/pydata-book",
    # "https://github.com/slundberg/shap",
    # "https://github.com/zergtant/pytorch-handbook",
    # "https://github.com/spmallick/learnopencv",
    # "https://github.com/fastai/fastbook"
]


def move_ipynb(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)
    for root, dirs, files in os.walk(directory + tmp_directory_suffix):
        for current_file in files:
            if current_file.lower().endswith('.ipynb'):
                location_from = f"{root}/{current_file}"
                location_to = f"{directory}/{current_file}"
                # print(f"File {location_from} moved to {location_to}")
                os.rename(location_from, location_to)


def delete_directory(directory: str) -> None:
    shutil.rmtree(directory)
    print(f"{directory} deleted.")


def clean_repository(directory: str) -> None:
    # Move all the .ipynb files to the final directory.
    move_ipynb(directory)

    # Delete the temporary directory.
    delete_directory(directory + tmp_directory_suffix)


def download_zip(repo: dict[str, str]) -> Response:
    response = requests.get(f"https://api.github.com/repos/{repo['owner']}/{repo['repo']}")
    if response.status_code != 200:
        raise Exception("Error while getting the most popular repositories on GitHub.")

    json_response = response.json()
    # print(f"json_response = {json_response}")
    default_branch = json_response['default_branch']
    download_url = f"https://github.com/{repo['owner']}/{repo['repo']}/archive/refs/heads/{default_branch}.zip"
    print(f"Downloading {download_url}")
    return requests.get(download_url)


def get_repositories() -> None:
    """
    Retrieve the URL of the top 10 most stars repositories on GitHub.
    """
    for repo in repositories:
        if os.path.exists(f"../notebooks/github/{repo['owner']}"):
            print(f"{repo['owner']} already created, this GitHub repository is skipped.")
            continue
        if os.path.exists(f"../notebooks/github/{repo['owner']}{tmp_directory_suffix}"):
            print(f"{repo['owner']}{tmp_directory_suffix} already created, skip the download part and retrieves the "
                  f"current notebooks.")
        else:
            zip_response = download_zip(repo)
            print("Extracting archive...")
            zip_file = zipfile.ZipFile(io.BytesIO(zip_response.content))
            zip_file.extractall(f"../notebooks/github/{repo['owner']}{tmp_directory_suffix}")
            print(f"{repo['owner']} directory extracted.")

        clean_repository(f"../notebooks/github/{repo['owner']}")


get_repositories()
