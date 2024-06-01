from database import PaperDao
from search.metadata_index import MetadataIndex
from search.main_conclusion_index import MainConclusionIndex
from search.disease_index import DiseaseIndex
from search.demographic_index import DemographicIndex
from search.combine_index import CombineIndex


# id_list = ['66575cc36d6b0aa04a1dbea3', '66575cc46d6b0aa04a1dbea4', '66575cc46d6b0aa04a1dbea5', '66575cc46d6b0aa04a1dbea6', '66575cc46d6b0aa04a1dbea7', '66575cc46d6b0aa04a1dbea8', '66575cc46d6b0aa04a1dbea9', '66575cc46d6b0aa04a1dbeaa', '66575cc46d6b0aa04a1dbeab', '66575cc46d6b0aa04a1dbeac', '66575cc46d6b0aa04a1dbead', '66575cc46d6b0aa04a1dbeae', '66575cc46d6b0aa04a1dbeaf']
# papers = [PaperDao.get(id) for id in id_list]

# papers = [PaperDao.get('66423b15a497602e0c390952')]
# print(papers)
papers = PaperDao.get_all()
print("Total", len(papers))

indices = [
    # MetadataIndex(),
    # MainConclusionIndex(),
    # DiseaseIndex(),
    # DemographicIndex(),
    CombineIndex()
]

for index in indices:
    index.create_embeddings(papers)
