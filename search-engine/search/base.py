from typing import List
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.schema import TextNode
from schemas import SearchItem, PaperResponse
from database.base import Database
import numpy as np
import faiss


class BaseIndex:
    def __init__(self, repo: Database):
        self.index = None
        self.retriever = None
        self.repo = repo
        self.node_type = "default"

    def query(self, query: str) -> List[SearchItem]:
        results = self.retriever.retrieve(query)
        items = []
        for item in results:
            item = SearchItem(**item.metadata)
            items.append(item)

        return items

    def create_embeddings(self, papers: List[PaperResponse]):
        '''
        Create embeddings for metadata of papers
        and save to database
        '''
        search_items = self.get_search_items(papers)
        content_str_list = [item.text for item in search_items]

        embeddings = self.embed_model.get_text_embedding_batch(
            content_str_list,
            show_progress=True
        )
        for item, embedding in zip(
            search_items,
            embeddings
        ):
            embedding = np.array(embedding)
            embedding /= np.linalg.norm(embedding)

            item.embedding = embedding.tolist()

            # save to db
            self.repo.insert(item)

        return embeddings

    def build_index(
        self,
        save_dir: str,
        top_k: int = 2,
    ):
        '''
        Create faiss index for local retrieval
        '''
        items = self.repo.get_all()
        nodes = []
        for item in items:
            if len(item.embedding) == 0:
                continue

            nodes.append(TextNode(
                text=item.text,
                metadata={
                    **{k: v for k, v in item.dict().items() if k != "embedding"},
                    "node_type": self.node_type
                },
                embedding=item.embedding
            ))

        faiss_index = faiss.IndexFlatIP(768)
        # Replace FAISS by Vector database
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            embed_model=self.embed_model
        )
        self.index.storage_context.persist(save_dir)
        self.retriever = self.index.as_retriever(similarity_top_k=top_k)

    def load_index(self, index_dir: str, top_k: int = 3):
        vector_store = FaissVectorStore.from_persist_dir(index_dir)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store, persist_dir=index_dir
        )
        self.index = load_index_from_storage(
            storage_context=storage_context,
            embed_model=self.embed_model
        )
        self.retriever = self.index.as_retriever(similarity_top_k=top_k)

