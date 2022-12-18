import io
import mmap
import os
import shutil
import time
import zipfile
from datetime import datetime

import requests
import tomli_w
from requests import Response

# Constants
TMP_DIRECTORY_SUFFIX = "-tmp"
OWNER = "owner"
NAME = "name"

# https://github.com/search?l=&o=desc&q=stars%3A%22%3E+1000%22+language%3A%22Jupyter+Notebook%22&s=stars&type=Repositories
links = {
    "https://github.com/microsoft/ML-For-Beginners",
    "https://github.com/aymericdamien/TensorFlow-Examples",
    "https://github.com/jakevdp/PythonDataScienceHandbook",
    "https://github.com/CompVis/stable-diffusion",
    "https://github.com/GokuMohandas/Made-With-ML",
    "https://github.com/google-research/google-research",
    "https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers",
    "https://github.com/ageron/handson-ml2",
    "https://github.com/ageron/handson-ml3",
    "https://github.com/fastai/fastai",
    "https://github.com/trekhleb/homemade-machine-learning",
    "https://github.com/MLEveryday/100-Days-Of-ML-Code",
    "https://github.com/chenyuntc/pytorch-book",
    "https://github.com/jupyter/notebook",
    "https://github.com/Atcold/pytorch-Deep-Learning",
}

repositories = []


def create_toml(directory: str, repository: dict[str, str]) -> None:
    for root, dirs, files in os.walk(directory):
        for current_file in files:
            if current_file.lower().endswith('.ipynb') and not os.path.isfile(f"{directory}/{current_file}.toml"):
                with open(f"{directory}/{current_file[:-6]}.toml", "wb") as file:
                    file_creation = os.path.getmtime(f"{directory}/{current_file}")
                    tomli_w.dump({'title': os.path.basename(file.name),
                                  'metadata':
                                      {
                                          'path': f"{os.path.relpath(file.name)}",
                                          'source': f"https://github.com/{repository[OWNER]}/{repository[NAME]}",
                                          'author': repository[OWNER],
                                          'date': datetime.fromtimestamp(file_creation).strftime("%d/%m/%Y")
                                      }
                                  }, file)


def file_contains_code(location_from) -> bool:
    if os.stat(location_from).st_size == 0:
        return False
    with open(location_from, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        if s.find(b'"cell_type": "code"') != -1:
            # Code found, the Jupyter Notebook contains code.
            return True
        # Code not found, the Jupyter Notebook does not contain code.
        return False


def move_ipynb(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)
    for root, dirs, files in os.walk(directory + TMP_DIRECTORY_SUFFIX):
        for current_file in files:
            if current_file.lower().endswith('.ipynb'):
                location_from = f"{root}/{current_file}"
                location_to = f"{directory}/{current_file}"
                if not os.path.isfile(location_to) and file_contains_code(location_from):
                    stat = os.stat(location_from)
                    os.rename(location_from, location_to)
                    os.utime(location_to, (stat.st_atime, stat.st_mtime))


def delete_directory(directory: str) -> None:
    shutil.rmtree(directory)
    print(f"{directory} deleted.")


def clean_repository(directory: str) -> None:
    # Move all the .ipynb files to the final directory.
    move_ipynb(directory)

    # Delete the temporary directory.
    delete_directory(directory + TMP_DIRECTORY_SUFFIX)


def download_zip(repository: dict[str, str]) -> Response:
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get('GITHUB_TOKEN') is not None:
        headers['Authorization'] = f"Bearer {os.environ.get('GITHUB_TOKEN')}"
    response = requests.get(f"https://api.github.com/repos/{repository[OWNER]}/{repository[NAME]}", headers)
    if response.status_code != 200:
        raise Exception("Error while getting the most popular repositories on GitHub.")

    json_response = response.json()
    # print(f"json_response = {json_response}")
    default_branch = json_response['default_branch']
    download_url = f"https://github.com/{repository[OWNER]}/{repository[NAME]}/archive/refs/heads/{default_branch}.zip"
    print(f"Downloading {download_url}")
    return requests.get(download_url)


def parse_links() -> None:
    for link in links:
        link = link.split('/')
        owner = link[3]
        name = ''.join(link[4:])
        repositories.append({OWNER: owner, NAME: name})


def get_directory_str(repository: dict[str, str]) -> str:
    if len(repository) == 2:
        return f"{repository[OWNER]}-{repository[NAME]}"
    return "unknown-repository"


def extract_zip(repository: dict[str, str]) -> None:
    directory = get_directory_str(repository)
    zip_response = download_zip(repository)
    print("Extracting archive...")

    zip_file = zipfile.ZipFile(io.BytesIO(zip_response.content))
    for zi in zip_file.infolist():
        zip_file.extract(zi, path=f"notebooks/github/{directory}{TMP_DIRECTORY_SUFFIX}")
        date_time = time.mktime(zi.date_time + (0, 0, -1))
        try:
            os.utime(f"notebooks/github/{directory}{TMP_DIRECTORY_SUFFIX}/{zi.filename}", (date_time, date_time))
        except Exception as e:
            # Handle weird filename.
            print(e)
    zip_file.close()

    print(f"{directory} directory extracted.")


def get_repositories() -> None:
    """
    Retrieve the notebooks of the top 10 most stars repositories on GitHub.
    """
    parse_links()

    for repository in repositories:
        directory = get_directory_str(repository)
        print(directory)

        if os.path.exists(f"notebooks/github/{directory}"):
            print(f"{repository[OWNER]} already created, this GitHub repository is skipped.")
            continue
        if os.path.exists(f"notebooks/github/{directory}{TMP_DIRECTORY_SUFFIX}"):
            print(f"{directory}{TMP_DIRECTORY_SUFFIX} already created, skip the download "
                  f"part and retrieves the current notebooks.")
        else:
            extract_zip(repository)

        clean_repository(f"notebooks/github/{directory}")
        create_toml(f"notebooks/github/{directory}", repository)


if __name__ == '__main__':
    get_repositories()
