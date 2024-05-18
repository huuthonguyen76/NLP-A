# Information Extraction
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
MODEL_NAME="gpt-3.5-turbo"
```
4. Run the data extraction for all document in DB
```
python ./main.py
```
