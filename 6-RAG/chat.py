
"""
This code demonstrates a Retrieval-Augmented Generation (RAG) approach 
using OpenAI's GPT-4o-mini model and a Qdrant vector store for information retrieval.
The code consists of two main parts:
1. INDEXING PHASE - Document Processing and Vector Store Creation (index.py):
    - Loads a PDF document, splits it into smaller chunks, and creates vector embeddings for those chunks.
    - Stores the embeddings in a Qdrant vector database for efficient retrieval.

2. RETREIVAL PHASE - Querying and Response Generation (chat.py):
    Steps:
    - Take user's query
    - Create Vector Embeddings for the query
    - Do Similarity search in the vector store to retrieve relevant chunks
    - Construct a system prompt that includes the retrieved chunks and their metadata
    - Use LLM to generate a response based on the system prompt and user query.

Make sure to have the necessary libraries installed and a Qdrant instance running locally to execute this code successfully.
"""
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model, 
    url = "http://localhost:6333",
    collection_name="learning_ RAG"
)

# User input query
query = "What are the design patterns mentioned in the document?"
# Retrieve relevant chunks from the vector store based on the query
retrieved_chunks = vector_store.similarity_search(query, top_k=5)  # Retrieve the top 5 most similar chunks
print("Retrieved Chunks:")
for i, chunk in enumerate(retrieved_chunks):
    print(f"Chunk {i+1}: {chunk.page_content[:500]}")  # Print the first 500 characters of each retrieved chunk's content

context = "\n\n\n".join([f"Page Content: {chunk.page_content}\n Page Number: {chunk.metadata['page_label']}\n File Location: {chunk.metadata['source']}"
                         for chunk in retrieved_chunks])  # Combine the content and metadata of the retrieved chunks into a single context string

SYSTEM_PROMPT = f"""You are a helpful assistant that provides information about design patterns based on the retrieved chunks 
from the document along with page_contents & metadata. Use the retrieved chunks to answer the user's query. If the information is not available 
in the retrieved chunks, respond with "I don't have that information.

Context:
{context}

"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
)

print("Response from the assistant:")
print(response.choices[0].message.content)