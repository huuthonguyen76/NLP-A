import urllib
import math
from bs4 import BeautifulSoup
from typing import List, Tuple
from utils.download import get_page_content
from utils.common import find_impact_factor
from .base import BaseCrawler
from schemas import Author


class BioMedCrawler(BaseCrawler):
    def __init__(self):
        super(BioMedCrawler, self).__init__()
        self.domain = "https://www.biomedcentral.com"
        self.search_suffix = "/search?searchType=publisherSearch&query="
        self.items_per_page = 20

    def get_paper_links(self, keywords: str, top_k: int) -> List[str]:
        """
        Retrieve the list paper links from the search engine
        Args:
            keywords (str): keywords to be searched

        Returns:
            papers (List[str]): list of paper metadata
        """
        top_k *= 5
        url = f"{self.domain}{self.search_suffix}{keywords}"
        soup = get_page_content(url)
        if soup is None:
            return []

        total_page = 1
        p_tag = soup.find("p", class_="u-text-sm u-reset-margin")
        if p_tag:
            total_page = int(p_tag.text.split(" ")[-1]
                             .replace(",", "").strip())

        print("[BioMed] Total Pages", total_page)
        target_page = min(total_page, math.ceil(top_k / self.items_per_page))
        print("[BioMed] Target Page", target_page)

        papers = []
        for i in range(1, target_page+1):
            if i > 1:
                url = f"{self.domain}{self.search_suffix}{keywords}&page={i}"
                soup = get_page_content(url)
                if soup is None:
                    print("[BioMed] Cannot load page", url)
                    continue

            for h3_tag in soup.find_all("h3", class_="c-listing__title"):
                try:
                    a_tag = h3_tag.find("a")
                    suffix = a_tag["href"]
                    papers.append(f"{self.domain}{suffix}")
                except Exception as e:
                    print(e)

                if len(papers) >= top_k:
                    break

        print(f"[BioMed] Found {len(papers)} links")
        return papers

    def find_doi(self, soup) -> str:
        """
        Extract DOI from HTML
        """
        for span_tag in soup.find_all(
            "span",
            class_="c-bibliographic-information__value"
        ):
            if "doi.org" in span_tag.text:
                doi = span_tag.text
                doi = doi.replace("https://doi.org/", "").lstrip("/")
                # convert special characters like %2 to /
                doi = urllib.parse.unquote(doi)
                return doi

        return ""

    def find_pmid(self, soup) -> str:
        """
        Extract PMID from HTML for PubMed articles
        """
        # not available in BioMed
        return ""

    def find_title(self, soup: BeautifulSoup) -> str:
        """
        Extract title from HTML
        """
        h1_tag = soup.find("h1", class_="c-article-title")
        if h1_tag:
            return h1_tag.text

        return ""

    def find_authors(self, soup: BeautifulSoup) -> List[Author]:
        """
        Extract authors as string from HTML
        """
        ol_tag = soup.find("ol", class_="c-article-author-affiliation__list")
        author_dicts = {}
        if ol_tag:
            for li_tag in ol_tag.find_all("li"):
                aff_tag = li_tag.find("p", class_="c-article-author-affiliation__address")
                authors_tag = li_tag.find("p", class_="c-article-author-affiliation__authors-list")
                if not aff_tag or not authors_tag:
                    continue
                affiliation = aff_tag.text
                authors = authors_tag.text.replace("&", ",").split(",")
                for author in authors:
                    author = author.strip()
                    if author == "":
                        continue

                    if author in author_dicts:
                        author_dicts[author].affiliations.append(affiliation)
                    else:
                        author_dicts[author] = Author(
                            name=author,
                            affiliations=[affiliation]
                        )

        return list(author_dicts.values())

    def find_journal_and_impact_factor(self, soup: BeautifulSoup) -> Tuple[str, float]:
        """
        Find impact factor of the journal of this article using ISSN
        """
        # journal name
        journal_title = ""
        span_tag = soup.find("span", class_="c-journal-title__text")
        if span_tag:
            journal_title = span_tag.text

        # journal ISSN
        p_tag = soup.find("p", class_="c-journal-footer__issn")
        if p_tag:
            issn = p_tag.text.replace("ISSN: ", "").strip()
            impact_factor = find_impact_factor(issn)
            if journal_title == "":
                journal_title = issn
            return journal_title, impact_factor
        return "", -1

    def find_publication_year(self, soup) -> str:
        """
        Extract year of publication from HTML
        """
        for li_tag in soup.find_all(
            "li",
            class_="c-article-identifiers__item"
        ):
            if "Published: " in li_tag.text:
                year = li_tag.text.strip().split(" ")[-1]
                return year
        return ""

    def find_pdf_link(self, soup: BeautifulSoup) -> str:
        """
        Extract PDF link from HTML
        """
        a_tag = soup.find("a", class_="c-pdf-download__link")
        if a_tag:
            pdf_suffix = a_tag["href"]
            pdf_link = f"{self.domain}{pdf_suffix}"
            return pdf_link
        return ""

