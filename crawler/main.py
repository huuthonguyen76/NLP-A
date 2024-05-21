import argparse
from database import PaperDao
from crawlers import PubMedCrawler, BioMedCrawler
from utils.download import download_papers
from utils.common import papers_to_database_item


def run(query, args):
    biomed_crawler = BioMedCrawler()
    pubmed_crawler = PubMedCrawler()

    print(f"Searching '{query}'...")

    papers = biomed_crawler.search(query, top_k=args.topk)
    dois = set([p.doi for p in papers])
    papers += pubmed_crawler.search(
        query,
        top_k=args.topk - len(papers),
        old_dois=dois
    )

    print(f"Found {len(papers)} papers:")
    for i, paper in enumerate(papers):
        print(f"{i+1}. {paper.title}")
    print()

    if args.interactive:
        pdf_save_dir = input(f"Enter directory path to save pdf files (default: {args.pdf_save_dir}):")
        if pdf_save_dir.strip() == "":  # default
            pdf_save_dir = args.pdf_save_dir
    else:
        pdf_save_dir = args.pdf_save_dir

    print("Downloading PDF files...")
    downloaded_papers = download_papers(papers, pdf_save_dir)
    print(f"Downloaded {len(downloaded_papers)} papers to {pdf_save_dir}.")
    for i, paper in enumerate(downloaded_papers):
        print(f"{i+1}. {paper.title}")
    print()

    print("Parsing PDF files...")
    items = papers_to_database_item(downloaded_papers)
    print("Done parsing PDF files.")

    print("Writing to MongoDB...")
    for item in items:
        PaperDao.insert(item)
    print("Done writing db.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', type=str, default="biometric",
                        help='Keyword query to search for Biology-related papers. Only used if interactive mode is False.')
    parser.add_argument('-k', '--topk', type=int, default=2,
                        help='Maximum number of papers to search')
    parser.add_argument('--pdf_save_dir', type=str, default="data/pdf",
                        help='Directory path to store PDF files')
    parser.add_argument('-i', '--interactive', action='store_true', default=False,
                        help='Use interactive mode.')

    args = parser.parse_args()

    if args.interactive:
        while True:
            print('=' * 20)
            query = input("Enter your keywords (Type 'q' to quit): ")
            query = query.strip()
            if query == 'q':
                break
            run(query=query, args=args)
            print()
    else:
        run(query=args.query, args=args)


if __name__ == "__main__":
    main()
