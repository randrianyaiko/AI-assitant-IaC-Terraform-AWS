from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def getGoogleEmbeddingFunction():
    embeddings = GoogleGenerativeAIEmbeddings(model = os.getenv("GOOGLE_EMBEDDING_MODEL"), 
                                          api_key=os.getenv("GOOGLE_GENAI_API_KEY"))
    return embeddings