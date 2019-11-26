import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_link(link):
    url = link
    resource = requests.get(url)
    soup = BeautifulSoup(resource.text, 'html.parser')
    return soup


def get_downloadable(link):
    soup = parse_link(link)
    downloadable_files = soup.find_all("a", {"class": "downloadline"})

    for file in downloadable_files:
        file_link = file.get("href")

        if file_link.split(".")[-1] != "html":
            print(urljoin(link, file_link))


def get_all_downloadable(link):
    soup = parse_link(link)
    downloadable_files = soup.find_all("a", href=True)

    for file in downloadable_files:
        file_link = file.get("href")

        if file_link.split(".")[-1] == "exe" or file_link.split(".")[-1] == "zip":
            print(urljoin(link, file_link))


def get_links():
    base_url = "http://3.228.218.197/"
    soup = parse_link(base_url)
    index_links = soup.find_all("a", href=True)

    for link in index_links:
        href = link.get("href")
        # get_downloadable(base_url+href)
        get_all_downloadable(base_url+href)


def main():
    get_links()


if __name__ == '__main__':
    main()