from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

Pdf_path = Path(__file__).parent / "DesignPattern.pdf"

# Load the PDF document using PyPDFLoader
loader = PyPDFLoader(file_path=Pdf_path)
docs = loader.load()  # This will load the PDF and split it into pages

print(f"Total pages loaded: {len(docs)}")
print(f"Content of the third page: {docs[2].page_content[:500]}")  # Print the first 500 characters of the third page's content

# split the docs into smaller chunks or smaller pieces
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
# chunk_size is the maximum number of characters in each chunk, and chunk_overlap is the number of characters that will overlap between consecutive chunks. This helps to maintain context when splitting the document into smaller pieces.
chunks = text_splitter.split_documents(docs)
print(f"Total chunks created: {len(chunks)}")
print(f"Content of the first chunk: {chunks[0].page_content[:500]}")  # Print the first 500 characters of the first chunk's content


# Vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
vector_store = QdrantVectorStore.from_documents(
    documents=chunks, 
    embedding=embedding_model, 
    url = "http://localhost:6333",
    collection_name="learning_ RAG"
)

print("Documents have been embedded and stored in the vector database.")
