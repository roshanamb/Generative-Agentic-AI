import json

from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "text-embedding-3-small" }
    },

    "llm": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "gpt-3.5-turbo" }
    },

    "vector_store": {
        "provider": "qdrant",
        "config": { "host": "localhost", "port": 6333 }
    },

    "graph_store": {
        "provider": "redisgraph",
        "config": { 
            "url": "neo4j+s://xxxxxxx.databases.neo4j.io",
            "username": "neo4j",
            "password": "xxxxxxx"
        }
    }
}  

mem_client = Memory.from_config(config)

while True:
    user_query = input("> ") 
    search_memories = mem_client.search(user_id="user_123", query=user_query, top_k=5)

    memories = [
        f"ID: {mem['id']} \n Memory: {mem['memory']} \n Metadata: {mem['metadata']}" 
        for mem in search_memories.get("results")
    ]
    print("Relevant memories from the memory store:", memories)

    SYSTEM_PROMPT = f"""
    You are a helpful assistant. Use the following relevant memories to answer the question as best as you can. 
    If you don't know the answer, say you don't know. Relevant memories: {json.dumps(memories)}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )
    api_response = response.choices[0].message.content
    print("API response:", api_response)

    mem_client.add(
        user_id="user_123",
        messages=[
            {"role": "user", "content": user_query}, 
            {"role": "assistant", "content": api_response}
        ]
    )

    print("Memory store updated with the above conversation.")