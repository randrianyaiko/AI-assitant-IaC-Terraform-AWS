from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_markdown(path: str) -> list:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    loader = UnstructuredMarkdownLoader(path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs
