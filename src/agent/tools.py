from src.vectordatabase.vectorstore import VectorStore

vectorstore = VectorStore()
def format_search_results(query, documents):
    results = "\n".join(doc.page_content for doc in documents)
    formatted_result = f"Search query: {query}\nResults: {results}"
    return formatted_result

def search(query: str, k: int = 10):
    """ Use this search tool to search on the documentation. """
    
    print(f"Searching for: {query}")    
    documents = vectorstore.search(query, k=k)
    formatted_result = format_search_results(query, documents)
    return formatted_result
