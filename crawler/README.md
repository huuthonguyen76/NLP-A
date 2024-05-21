# Paper Crawler
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
```
4. Start querying by specifying the query via -q and number of papers via -k.
```
python main.py -q "gut microbiome" -k 100
```
