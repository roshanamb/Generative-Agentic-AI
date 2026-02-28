
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

# Load the existing vector store from Qdrant
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model, 
    url = "http://localhost:6333",
    collection_name="learning_ RAG"
)

def process_query(query: str):
    print(f"Searching chunks for query: {query}")
    # Retrieve relevant chunks from the vector store based on the query
    retrieved_chunks = vector_store.similarity_search(query, top_k=5)  # Retrieve the top 5 most similar chunks

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
    print("Response from the assistant:", response.choices[0].message.content)

