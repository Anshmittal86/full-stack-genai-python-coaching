from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

# Breaking into pages
file_path = "./nodejs.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()

# Breaking pages into smaller text (chunks)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents=docs)
print(chunks)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="learning-rag",
    embedding=embedding_model
)

vector_store.add_documents(chunks)

print("Indexing is done....")
