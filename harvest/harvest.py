# thursday: verify download duplicate | save to db | verify index updates | *start api
import requests
from requests import get
import re
import configparser
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import harvest_database as db

config = configparser.ConfigParser()
conf_dir = os.path.join(os.path.dirname(__file__), 'conf.ini')
config.read(conf_dir)
password = config['args']['password']
hostname = config['args']['hostname']
username = config['args']['username']
dbname = config['args']['dbname']


def parse_link(link):
    url = link
    resource = requests.get(url)
    soup = BeautifulSoup(resource.text, 'html.parser')
    return soup


def download_file(url, filename):
    with open(filename, "wb") as file:
        response = get(url)
        file.write(response.content)


def get_all_downloadable(link):
    soup = parse_link(link)
    name_version = get_details(link)
    db.insert_details(username, password, hostname, dbname, name_version)
    download_links = soup.find_all("a", href=True)
    acceptable_ext = ["exe", "zip"]
    downloadable_files = []
    for file in download_links:
        file_link = file.get("href")
        if file_link.split(".")[-1] in acceptable_ext:
            download_link = urljoin(link, file_link)
            downloadable_files.append(download_link)
            # download_file(download_link, name_version['name'])
    return downloadable_files


def check_version(link):
    name_version = get_details(link)
    if db.select_details(username, password, hostname, dbname, name_version):
        get_all_downloadable(link)


def get_details(download_link):
    soup = parse_link(download_link)
    version_regex = "v[0-9]*\.[0-9]*"
    details = soup.find(text=re.compile(version_regex))
    name_version = details.split("-")[0]
    index = re.search(version_regex, name_version)
    name = name_version[0:index.start()]
    version = name_version[index.start():]
    return {"name": name, "version": version}


def get_links():
    base_url = "http://54.174.36.110/"
    soup = parse_link(base_url)
    unordered_list = soup.find("ul")
    index_links = unordered_list.find_all("a", href=True)
    download_pages = []
    for link in index_links:
        href = link.get("href")
        if "http" not in href and href not in db.select_all_links(username, password, hostname, dbname):
            download_page_link = base_url + href  # url of the download page
            download_pages.append(download_page_link)  # get details of download pages then save to list
            check_version(download_page_link)  # checker of version changes
            db.insert_links(username, password, hostname, dbname, href)  # checker of link duplicates

    for pages in download_pages:
        check_version(pages)

    return download_pages


def main():
    get_links()


if __name__ == '__main__':
    main()
