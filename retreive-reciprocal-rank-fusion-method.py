from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor #Multithreading
from itertools import chain #Flatten
import ast #Parsing

load_dotenv()

client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning-rag",
    embedding=embedding_model
)

while True:
    user_query = input("👨: ")
    
    query_breakdown_prompt = """
        You are a helpful ai Assistant. Your task is to take the user query and breakdown the user query into different sub-queries.
        
        Rule:
        maximum Sub Query Length: 3
        
        Examples:
        query: How to become GenAI Developer?
        Output: [
            'What is GenAI?',
            'What is Developer',
            'How to become GenAI Developer'
        ]
        
    """
    
    response = client.chat.completions.create(
        model='gpt-5.2',
        messages=[
            { "role" : "system", "content": query_breakdown_prompt },
            { "role": "user", "content": user_query },
        ]
    )
    
    sub_queries = ast.literal_eval(response.choices[0].message.content.strip())
    # print(f"sub_quries: {sub_queries}")
    
    def retrieve_chunks(query: str):
        return vector_store.similarity_search(query=query)
    
    with ThreadPoolExecutor() as executor:
        all_chunks = list(executor.map(retrieve_chunks, sub_queries))
    
    flattened_chunks = list(chain.from_iterable(all_chunks))
    
    # Helper to generate a unique ID for each chunk (or you can use doc.metadata['id'] if available)
    def get_doc_id(doc):
        return doc.page_content.strip()[:50]
    
    # Create rankings (lists of doc_ids per sub-query result)
    rankings = []
    for result in all_chunks:
        rankings.append([get_doc_id(doc) for doc in result])
    
    # Reciprocal Rank Fusion
    def reciprocal_rank_fusion(rankings, k=60):
        scores = {}

        for ranking in rankings:
            for rank, doc_id in enumerate(ranking):
                scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, score in sorted_docs]

    # Get final ranked doc IDs
    final_doc_ids = reciprocal_rank_fusion(rankings)    
    
    # Map doc IDs to actual chunks
    doc_map = {get_doc_id(doc): doc for doc in chain.from_iterable(all_chunks)}
    ranked_chunks = [doc_map[doc_id] for doc_id in final_doc_ids if doc_id in doc_map]


    system_prompt = f"""
        You are a helpful assistant who answer user's query by using the following pieces of context with the page no. so that user can refer.
        If you don't know the answer, just say that I don't know with the reason why you are not able to give the answer only give the 2 to 3 line max reason instead of just saying I don't know, don't try to make up an answer.
        
        context: 
        {[doc.page_content for doc in ranked_chunks]}
    """

    response = client.chat.completions.create(
        model='gpt-5.2',
        messages=[
            { "role" : "system", "content": system_prompt },
            { "role": "user", "content": user_query },
        ]
    )

    pdf_response = response.choices[0].message.content

    print(f"🤖: {pdf_response }")