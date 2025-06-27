import os
import numpy as np
from typing import List, Tuple
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from summarize_webpage import webpage_summary

def cosine_similarity(vec1, vec2):
    """Compute cosine similarity between two vectors."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Load env vars
load_dotenv()

# Initialize Azure OpenAI Embeddings via LangChain
embedding_model = AzureOpenAIEmbeddings(
    api_key=os.getenv("azure_embedding_key"),
    openai_api_type="azure",
    azure_endpoint=os.getenv("azure_embedding_endpoint"),
    azure_deployment=os.getenv("azure_embedding_model"),
    dimensions=1024,
)

def enrich_with_embeddings(results: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str, List[float]]]:
    """Add embedding vector to each (id, link, description) tuple."""
    enriched = []
    descriptions = [desc for _, _, desc in results]
    vectors = embedding_model.embed_documents(descriptions)

    for (form_id, link, desc), vector in zip(results, vectors):
        enriched.append((form_id, link, desc, vector))

    return enriched

def search_similar_forms(enriched_results: List[Tuple[str, str, str, List[float]]], query: str, top_k: int = 5) -> List[Tuple[str, str, str, float]]:
    """Search top_k most similar forms to the user query."""
    query_vector = embedding_model.embed_query(query)
    scored_results = []

    for form_id, link, desc, vec in enriched_results:
        similarity = cosine_similarity(np.array(query_vector), np.array(vec))
        scored_results.append((form_id, link, desc, similarity))

    # Sort by similarity descending
    scored_results.sort(key=lambda x: x[3], reverse=True)
    return scored_results[:top_k]


def search_from_query(query):
    results = webpage_summary()
    enriched = enrich_with_embeddings(results)
    top_k = 3
    top_k_similar = search_similar_forms(enriched, query = query, top_k=top_k)
    fin = [f"{count}. id: {tup[0]}\n, link: {tup[1].split('/')[-2:]}\n, description: {tup[2]}\n\n\n" for count,tup in enumerate(top_k_similar)]
    return fin

# #todo - vector search the forms and return link
# def search_form_index(query):
#     # pretend we return a list of forms with titles + ids
#     return [
#         {"id": "form_001", "title": "tax declaration form"},
#         {"id": "form_002", "title": "passport renewal form"},
#         {"id": "form_003", "title": "voter registration form"},
#     ]