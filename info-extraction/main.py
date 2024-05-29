from time import time
from database import PaperDao
from extractors import InformationExtractor


id_list = ['66575cc36d6b0aa04a1dbea3', '66575cc46d6b0aa04a1dbea4', '66575cc46d6b0aa04a1dbea5', '66575cc46d6b0aa04a1dbea6', '66575cc46d6b0aa04a1dbea7', '66575cc46d6b0aa04a1dbea8', '66575cc46d6b0aa04a1dbea9', '66575cc46d6b0aa04a1dbeaa', '66575cc46d6b0aa04a1dbeab', '66575cc46d6b0aa04a1dbeac', '66575cc46d6b0aa04a1dbead', '66575cc46d6b0aa04a1dbeae', '66575cc46d6b0aa04a1dbeaf']
papers = [PaperDao.get(id) for id in id_list]
# print(papers)
# papers = PaperDao.get_all()
info_extractor = InformationExtractor()
for i, paper in enumerate(papers):
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
