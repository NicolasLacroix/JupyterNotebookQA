import re

import requests
from bs4 import BeautifulSoup


def get_repositories() -> list[str]:
    """
    Retrieve the URL of the top 10 most stars repositories on GitHub.
    :return: A list of URL.
    """
    search_url = "https://github.com/search?l=&o=desc&p=2&q=stars%3A%22%3E+1000%22+language%3A%22Jupyter+Notebook%22&s" \
                 "=stars&type=Repositories"
    response = requests.get(search_url)
    if response.status_code != 200:
        raise Exception("Error while getting the most popular repositories on GitHub.")

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", class_="v-align-middle")

    result = []
    for element in links:
        url_github = re.match(r"url\":\"https://github\.com/(\w+)\"", str(element.text))
        href = re.match(r"href=\"/Pierian-Data/Complete-Python-3-Bootcamp", str(element.text))
        if url_github is not None:
            print(f"URL group 0 : {url_github.group(1)}")
        if href is not None:
            print(f"href group 0 : {href.group(1)}")

            if url_github is not None and href is not None and url_github.group(1) == href.group(1):
                print(url_github.group(1))
                result.append(url_github.group(1))

    return result


url = get_repositories()
print("After filter: ")
print(url)
