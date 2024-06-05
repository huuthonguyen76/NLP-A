### Generative AI - Paper Search
- **Paper Crawler**: See [Instructions](./crawler/README.md)
- **Information Extraction**: See [Instructions](./info-extraction/README.md)
- **Search Engine**: See [Instructions](./search-engine/README.md)

### TODOs
- [ ] Replace FAISS by real Vector Database.  
- [ ] Write cutom prompt to extract and parse relevant scores for LLM Reranking  
- [ ] Find optimal batch size for LLM Reranking  
- [ ] Find better ways to format the text to create embeddings for each index.  
- [ ] Enhance the prompt for query formulation (split the original query to sub queries for each index)  
- [ ] Find better way to calculate the aggregated scores (instead of just summing) for the chunks that belong to the same paper.  
