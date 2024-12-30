file_path = "nke-10k-2023.pdf"
"""
PyPDFLoader is one example of doc loaders. There are a whole bunch of document loaders.
Checkout more here: https://python.langchain.com/docs/how_to/#document-loaders
"""
from langchain_community.document_loaders import PyPDFLoader

# todo - load documents from other kinds of stores later on
loader = PyPDFLoader(file_path)
docs = loader.load()
print(len(docs))
print(f"{docs[0].page_content[:200]}\n")
print(docs[0].metadata)

"""
Text Splitting
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
print(len(all_splits))

"""
Embeddings
"""
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])

"""
Vector Stores
"""

from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=all_splits)
print(ids)

results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the United States of America?"
)

print(results)

"""
Retrievers - implement runnables but vector stores do not
"""
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import chain


@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)


retrieval = retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)

print(retrieval)


