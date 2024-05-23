import os
from time import time
from search.metadata_index import MetadataIndex
from search.main_conclusion_index import MainConclusionIndex
from search.disease_index import DiseaseIndex
from search.demographic_index import DemographicIndex


out_dir = "./data/index"
os.makedirs(out_dir, exist_ok=True)

indices = {
    "metadata": MetadataIndex(),
    "main_conclusion": MainConclusionIndex(),
    "disease": DiseaseIndex(),
    "demographic": DemographicIndex()
}

for key, index in indices.items():
    st = time()
    print(f"Building {key} index...")
    index.build_index(save_dir=os.path.join(out_dir, key))
    print(f"Done in {time() - st}.")
