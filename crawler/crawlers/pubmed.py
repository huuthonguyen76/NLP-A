import math
import urllib
from bs4 import BeautifulSoup
from typing import List, Tuple
from utils.download import get_page_content
from utils.common import find_impact_factor
from .base import BaseCrawler
from schemas import Author


class PubMedCrawler(BaseCrawler):
    def __init__(self):
        super(PubMedCrawler, self).__init__()
        self.domain = "https://www.ncbi.nlm.nih.gov"
        self.search_suffix = "/pmc/?term="
        self.items_per_page = 20

    def get_paper_links(self, keywords: str, top_k: int) -> List[str]:
        """
        Retrieve the list paper links from the search engine
        Args:
            keywords (str): keywords to be searched

        Returns:
            papers (List[str]): list of paper metadata
        """
        url = f"{self.domain}{self.search_suffix}{keywords}"
        soup = get_page_content(url)
        if soup is None:
            return []

        total_page = 1
        label_tag = soup.find("h3", class_="page")
        if label_tag:
            total_page = int(label_tag.text.split(" ")[-1]
                             .replace(",", "").strip())

        print("[PubMed] Total Pages", total_page)
        target_page = min(total_page, math.ceil(top_k / self.items_per_page))
        print("[PubMed] Target Page", target_page)

        papers = []
        for i in range(1, target_page+1):
            if i > 1:
                url = f"{self.domain}{self.search_suffix}{keywords}&page={i}"
                soup = get_page_content(url)
                if soup is None:
                    print("[PubMed] Cannot load page", url)
                    continue

            for div_tag in soup.find_all("div", class_="rprt"):
                try:
                    a_tag = div_tag.find("a")
                    suffix = a_tag["href"]
                    papers.append(f"{self.domain}{suffix}")
                except Exception as e:
                    print(e)

                if len(papers) >= top_k:
                    break

        print(f"[PubMed] Found {len(papers)} links")
        return papers

    def find_doi(self, soup) -> str:
        """
        Extract DOI from HTML
        """
        span_tag = soup.find("span", class_="doi")
        if span_tag and span_tag.find("a"):
            doi = span_tag.a["href"]
            doi = doi.replace("doi.org", "").lstrip("/")
            # convert special characters like %2 to /
            doi = urllib.parse.unquote(doi)
            return doi
        return ""

    def find_pmid(self, soup) -> str:
        """
        Extract PMID from HTML for PubMed articles
        """
        for div_tag in soup.find_all("div", class_="fm-citation-pmid"):
            if "PMID:" in div_tag.text:
                try:
                    pmid = div_tag.a.text
                    return pmid
                except Exception as e:
                    print(e)
        return ""

    def find_title(self, soup: BeautifulSoup) -> str:
        """
        Extract title from HTML
        """
        h1_tag = soup.find("h1", class_="content-title")
        if h1_tag:
            title = h1_tag.text
            return title
        return ""

    def find_authors(self, soup: BeautifulSoup) -> List[Author]:
        """
        Extract authors as string from HTML
        """

        # find affiliations
        affiliation_dict = {}
        div_tag = soup.find("div", class_="fm-authors-info")
        if div_tag:
            for tag in div_tag.find_all("div", class_="fm-affl"):
                sup_tag = tag.find("sup")
                if sup_tag:
                    sup_text = sup_tag.text.strip()
                    affiliation_dict[sup_text] = tag.text[len(sup_text):].strip()

        # find authors
        authors = []
        div_tag = soup.find("div", class_="contrib-group fm-author")
        author = None
        aff = []
        if div_tag:
            for tag in div_tag.children:
                if tag.name == "a":
                    if author is not None:
                        authors.append(Author(
                            name=author,
                            affiliations=aff
                        ))
                    author = tag.text
                    aff = []
                elif tag.name == "sup":
                    sup_name = tag.text.strip().strip(",").strip()
                    if author is not None and sup_name in affiliation_dict:
                        aff.append(affiliation_dict[sup_name])
            if author is not None:
                authors.append(Author(
                    name=author,
                    affiliations=aff
                ))

        return authors

    def find_journal_and_impact_factor(self, soup: BeautifulSoup) -> Tuple[str, float]:
        """
        Find impact factor of the journal of this article using ISSN
        """
        div_tag = soup.find("div", class_="fm-citation")
        if not div_tag:
            return "", -1

        div_tag = div_tag.find("div", class_="part1")
        if not div_tag:
            return "", -1

        span_tag = div_tag.find("span")
        if not span_tag:
            return "", -1

        journal_name = span_tag.text.strip(".")
        impact_factor = find_impact_factor(journal_name)

        return journal_name, impact_factor

    def find_publication_year(self, soup) -> str:
        """
        Extract year of publication from HTML
        """
        span_tag = soup.find("span", class_="fm-vol-iss-date")
        if span_tag:
            year = span_tag.text
            year = year.replace("Published online ", "").strip().split(" ")[0]
            return year
        return ""

    def find_pdf_link(self, soup: BeautifulSoup) -> str:
        """
        Extract PDF link from HTML
        """
        li_tag = soup.find("li", class_="pdf-link")
        if li_tag and li_tag.find("a"):
            pdf_suffix = li_tag.a["href"]
            pdf_link = f"{self.domain}{pdf_suffix}"
            return pdf_link
        return ""
