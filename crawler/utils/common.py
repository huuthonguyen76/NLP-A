from tqdm import tqdm
from typing import List
from schemas import Paper, PaperItem
from pdf_parser.content_extraction import pdf_to_text
from impact_factor.core import Factor


fa = Factor()


def find_impact_factor(query: str):
    """
    query: issn, nlm_id, or journal name
    """
    results = fa.search(query)

    if len(results) > 0:
        return results[0].get('factor', -1)

    return -1


def papers_to_database_item(papers: List[Paper]) -> List[PaperItem]:
    """
    Extract paper content and convert Paper object to PaperItem to store in db
    """
    data = []

    # convert each PDF file to raw text
    for paper in tqdm(papers):
        text = pdf_to_text(paper.pdf_file_path)
        data.append(PaperItem(
            content=text,
            url=paper.paper_link,
            **paper.dict(),
        ))

    return data

