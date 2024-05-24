# Search Engine
## Installation
1. Create a virtual environment
```
conda create -n crawler python=3.11.9
conda activate crawler
```
2. Install dependencies.
```
pip install -r requirements.txt
```
3. Create the .env file and set the credentials for DB and OpenAI 
```
MONGODB_URI="Connection URL"
MONGODB_DATABASE_NAME="data-ingestion"

OPENAI_API_KEY="You OpenAI Key"
MODEL_NAME="gpt-4o"
```
4. (Skip if data is already available in DB) Create embeddings and save to DB
```
python ./build_index_for_db.py
```
5. Build the local index (fetch embeddings from MongoDB and build local FAISS index)
```
python ./build_local_index.py
```
6. Run the search engine
```
python ./main.py
```
