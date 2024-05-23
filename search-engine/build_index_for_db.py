from database import PaperDao
from search.metadata_index import MetadataIndex
from search.main_conclusion_index import MainConclusionIndex
from search.disease_index import DiseaseIndex
from search.demographic_index import DemographicIndex


# papers = [PaperDao.get('66423a06761089191a2797f7')]
papers = [PaperDao.get('66423b15a497602e0c390952')]
print(papers)
papers = PaperDao.get_all()
print("Total", len(papers))

indices = [
    MetadataIndex(),
    MainConclusionIndex(),
    DiseaseIndex(),
    DemographicIndex()
]

for index in indices:
    index.create_embeddings(papers)
