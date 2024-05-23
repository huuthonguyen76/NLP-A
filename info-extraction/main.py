from time import time
from database import PaperDao
from extractors import InformationExtractor


# papers = [PaperDao.get('66423b15a497602e0c390952')]
# print(papers)
papers = PaperDao.get_all()
info_extractor = InformationExtractor()
for i, paper in enumerate(papers):
    if i < 692:
        continue
    if paper.conclusions.main_conclusion.conclusion.strip() != "":
        continue

    st = time()
    print("=" * 10, f"Paper {i} / {len(papers)}", "=" * 10)
    print(paper.id)
    print(paper.title)

    # set verbose = False in order not to print any logs
    result = info_extractor.extract(paper.content, verbose=True)
    print("Elapse", time() - st)
    print()

    # uncomment this if you just want to test and dont want to update DB
    PaperDao.update(paper.id, result)
