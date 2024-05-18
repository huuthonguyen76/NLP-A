from time import time
from database import PaperDao
from extractors import InformationExtractor


# paper = PaperDao.get('66423a06761089191a2797f7')
papers = PaperDao.get_all()
info_extractor = InformationExtractor()
for i, paper in enumerate(papers):
    if i < 197:
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
