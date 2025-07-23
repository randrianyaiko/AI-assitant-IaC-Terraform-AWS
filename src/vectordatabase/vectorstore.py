from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, SparseVectorParams, VectorParams
from langchain_qdrant import FastEmbedSparse, RetrievalMode
from dotenv import load_dotenv
from src.llm.embeddings import getGoogleEmbeddingFunction  # Assuming this is your dense embedding function
import os
import uuid

load_dotenv()

class VectorStore:
    def __init__(self):
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME")

        # Connect to Qdrant
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        self.sparse_embedding = FastEmbedSparse(model_name="Qdrant/bm25")

        self._init_collection()
        embeddings = getGoogleEmbeddingFunction()
        self.vectorstore = QdrantVectorStore(client=self.client,
                                             collection_name=self.collection_name,
                                             embedding=embeddings,
                                             sparse_embedding=self.sparse_embedding,
                                             retrieval_mode=RetrievalMode.HYBRID,
                                             vector_name="dense",
                                             sparse_vector_name="sparse"
                                             )
        
    def _init_collection(self):
        # Only create if it doesn't exist
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "dense": VectorParams(size=768, distance=Distance.COSINE)
                },
                sparse_vectors_config={
                    "sparse": SparseVectorParams(index=models.SparseIndexParams(on_disk=False))
                },
            )

    def add_documents(self, documents):
        """Add LangChain-compatible Document objects to the store."""
        ids = [str(uuid.uuid4()) for _ in documents]
        self.vectorstore.add_documents(documents=documents, ids=ids)

    def search(self, query: str, k: int = 10):
        """Perform hybrid search."""
        return self.vectorstore.similarity_search(query, k=k)

    def getRetriever(self):
        self.retriever = self.vectorstore.as_retriever()
        return self.retriever