import json
from tqdm import tqdm
from glob import glob
from database import PaperDao
from schemas import Paper
from utils.common import papers_to_database_item


def main():
    filelist = glob("../../pdf/*.pdf")
    papers = []
    for file in tqdm(filelist):
        json_file = file.replace(".pdf", ".json")
        with open(json_file, "r") as f:
            json_obj = json.load(f)
        paper = Paper.model_validate(json_obj)
        paper.pdf_file_path = file
        papers.append(paper)

    print("Parsing PDF files...")
    items = papers_to_database_item(papers)
    print("Done parsing PDF files.")
    print(items)

    print("Writing to MongoDB...")
    ids = []
    for item in items:
        id = PaperDao.insert(item)
        ids.append(str(id))
    print("Done writing db.")
    print(ids)
    # ['66575cc36d6b0aa04a1dbea3', '66575cc46d6b0aa04a1dbea4', '66575cc46d6b0aa04a1dbea5', '66575cc46d6b0aa04a1dbea6', '66575cc46d6b0aa04a1dbea7', '66575cc46d6b0aa04a1dbea8', '66575cc46d6b0aa04a1dbea9', '66575cc46d6b0aa04a1dbeaa', '66575cc46d6b0aa04a1dbeab', '66575cc46d6b0aa04a1dbeac', '66575cc46d6b0aa04a1dbead', '66575cc46d6b0aa04a1dbeae', '66575cc46d6b0aa04a1dbeaf']


if __name__ == "__main__":
    main()

