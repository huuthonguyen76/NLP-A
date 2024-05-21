from tqdm import tqdm
from typing import List, Optional, Tuple, Set
from utils.download import get_page_content
from bs4 import BeautifulSoup
from schemas import Paper


class BaseCrawler:
    domain: str

    def search(self, keywords: str, top_k: int = 10, old_dois: Set[str] = set()) -> List[Paper]:
        """
        Search by keywords and return paper results
        Args:
            keywords (str): keywords to be searched

        Returns:
            papers (List[Paper]): list of Paper objects
        """
        if top_k <= 0:
            return []

        # get the original paper urls
        temp = self.get_paper_links(keywords=keywords, top_k=top_k)

        # get the downloadable links
        print("Extracting metadata...")
        papers = []
        for paper_link in tqdm(temp):
            paper = self.get_paper_metadata(paper_link=paper_link)

            # ignore papers that are missing DOI/PMID and pdf_link
            if paper is None or \
                    (paper.doi.strip() == "" and paper.pmid.strip() == "") or \
                    paper.pdf_link.strip() == "":
                continue

            if paper.title.startswith("Correction"):
                print("Skip", paper.title)
                continue

            doi = paper.doi.strip()
            if doi != "" and doi in old_dois:
                continue

            papers.append(paper)

            if len(papers) >= top_k:
                break

        print(f"Filtered: {len(papers)} papers")
        return papers

    def get_paper_metadata(self, paper_link: str) -> Optional[Paper]:
        """
        Retrieve the paper metadata including DOI, title, author, and
        PDF downloadable link for the given paper
        Args:
            paper_link (str): the paper url

        Returns:
            result (dict): a dictionary object containing DOI, author,
                and PDF downloadable link for the given paper
        """
        soup = get_page_content(paper_link)
        if soup is None:
            return None

        journal, impact_factor = self.find_journal_and_impact_factor(soup)
        return Paper(
            doi=self.find_doi(soup),
            pmid=self.find_pmid(soup),
            title=self.find_title(soup),
            journal=journal,
            impact_factor=impact_factor,
            publication_year=self.find_publication_year(soup),
            authors=self.find_authors(soup),
            paper_link=paper_link,
            pdf_link=self.find_pdf_link(soup)
        )

    def get_paper_links(self, keywords: str, top_k: int) -> List[str]:
        """
        Retrieve the list paper links from the search engine
        Args:
            keywords (str): keywords to be searched

        Returns:
            papers (List[str]): list of paper metadata
        """
        raise NotImplementedError

    def find_doi(self, soup) -> str:
        """
        Extract DOI from HTML
        """
        raise NotImplementedError

    def find_pmid(self, soup) -> str:
        """
        Extract PMID from HTML for PubMed articles
        """
        raise NotImplementedError

    def find_title(self, soup: BeautifulSoup) -> str:
        """
        Extract title from HTML
        """
        raise NotImplementedError

    def find_authors(self, soup: BeautifulSoup) -> str:
        """
        Extract authors as string from HTML
        """
        raise NotImplementedError

    def find_journal_and_impact_factor(self, soup: BeautifulSoup) -> Tuple[str, float]:
        """
        Find impact factor of the journal of this article using ISSN
        """
        raise NotImplementedError

    def find_publication_year(self, soup) -> str:
        """
        Extract year of publication from HTML
        """
        raise NotImplementedError

    def find_pdf_link(self, soup: BeautifulSoup) -> str:
        """
        Extract PDF link from HTML
        """
        raise NotImplementedError
