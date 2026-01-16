# ONgoing 

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI
import json

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
    
    
    chain_of_thoughts_prompt="""
    
    You are helpful AI Assistant. 
    Your task is to create a step by step plan and think how to answer the user's Query
    and provide the output steps in JSON format. Last step should be the user query.

    Rule:
    1. Follow the strict JSON output as per Output schema.
    2. Always perform one step at a time and wait for next input
    3. Carefully analyse the user query
    4. Do not repeat the same step
    5. Perform Maximum 4 steps

    Example: 
    Query: What is FS Module in NodeJS?
    Output: {{ step: "thinking", content: "What is FS?" }}
    Output: {{ step: "thinking", content: "What is Module?" }}
    Output: {{ step: "thinking", content: "What is NodeJS?" }}
    Output: {{ step: "final_thinking", content: "What is FS Module in Nodejs?" }}

    """
    
    response = client.chat.completions.create(
        model='gpt-5.2',
        messages=[
            { "role" : "system", "content": chain_of_thoughts_prompt },
            { "role": "user", "content": user_query },
        ]
    )
    
    result = response.choices[0].message.content.strip()
    print(result)
    # Parse each block into dictionary
    step_thoughts = [json.loads(block) for block in result]
    print(step_thoughts)

    # system_prompt = f"""
    #     You are a helpful assistant who answer user's query by using the following pieces of context with the page no. so that user can refer.
    #     If you don't know the answer, just say that I don't know with the reason why you are not able to give the answer only give the 2 to 3 line max reason instead of just saying I don't know, don't try to make up an answer.
        
    #     context: {relevant_chunks}
    # """

    # response = client.chat.completions.create(
    #     model='gpt-5-mini',
    #     messages=[
    #         { "role" : "system", "content": system_prompt },
    #         { "role": "user", "content": user_query },
    #     ]
    # )

    # pdf_response = response.choices[0].message.content

    # print(f"🤖: {pdf_response }")