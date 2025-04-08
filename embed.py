# embed.py - Use OpenAI embeddings with latest OpenAI SDK (v1.x)

import os
import json
import numpy as np
import faiss
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("ini.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def embed_articles(company):
    input_path = f"data/processed/{company.lower().replace(' ', '_')}_scored.json"
    embed_path = f"data/processed/{company.lower().replace(' ', '_')}_openai_embeddings.npy"
    index_path = f"data/processed/{company.lower().replace(' ', '_')}_openai_faiss.index"

    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    embeddings = []
    for article in articles:
        content = article.get("content", "")
        embedding = get_openai_embedding(content)
        embeddings.append(embedding)

    embeddings = np.array(embeddings)
    np.save(embed_path, embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_path)

    print(f"Embedded and indexed {len(embeddings)} articles for {company} using OpenAI embeddings.")

if __name__ == "__main__":
    company = input("Enter company name to embed articles: ")
    embed_articles(company)
