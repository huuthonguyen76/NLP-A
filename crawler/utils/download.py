import os
from uuid import uuid4
from typing import List
import requests
import logging
from bs4 import BeautifulSoup
from tqdm import tqdm
from schemas import Paper


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def get_page_content(url) -> BeautifulSoup:
    if url.strip() == "":
        print("[get_page_content]: emtpy url")
        return None

    try:
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            return None
        html = res.text
        return BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(e)
        return None


def download_file(url, path_to_save) -> bool:
    """
    Download PDF files from the given link
    """
    if url.strip() == "":
        print("[download_file]: emtpy url")
        return False

    try:
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            logging.error(f"Cannot download PDF file from {url}")
            return False

        with open(path_to_save, 'wb') as file:
            file.write(res.content)

        return True
    except Exception as e:
        print(e)
        return False


def download_papers(
    papers: List[Paper],
    save_dir="./pdf_files"
) -> List[Paper]:
    """
    Download all papers in the list
    Args:
        papers (List[Paper]): list of Paper objects to be downloaded

    Returns:
        downloaded_papers (List[Paper]): list of downloaded papers
    """

    os.makedirs(save_dir, exist_ok=True)

    downloaded_papers = []
    for paper in tqdm(papers):
        title = paper.title.replace(" ", "-")
        save_path = os.path.join(save_dir, f"{uuid4()}.pdf")
        success = download_file(paper.pdf_link, save_path)
        if success:
            paper.pdf_file_path = save_path
            downloaded_papers.append(paper)

    return downloaded_papers
