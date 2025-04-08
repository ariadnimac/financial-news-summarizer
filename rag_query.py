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

def ask_question(company, query, top_k=3):
    embed_path = f"data/processed/{company.lower().replace(' ', '_')}_openai_embeddings.npy"
    index_path = f"data/processed/{company.lower().replace(' ', '_')}_openai_faiss.index"
    data_path = f"data/processed/{company.lower().replace(' ', '_')}_scored.json"

    embeddings = np.load(embed_path)
    index = faiss.read_index(index_path)

    with open(data_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    query_vec = np.array([get_openai_embedding(query)], dtype=np.float32)
    _, indices = index.search(query_vec, top_k)

    context = ""
    for i in indices[0]:
        article = articles[i]
        context += f"\nTitle: {article['title']}\nContent: {article['content']}\n"

    prompt = f"Based on the following news articles, answer the question: '{query}'\n{context}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    return answer

if __name__ == "__main__":
    company = input("Enter company name: ")
    query = input("Ask a question about the news: ")
    ask_question(company, query)
