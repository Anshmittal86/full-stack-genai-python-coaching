from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Breaking into pages
file_path = "./nodejs.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()

# Breaking pages into smaller text (chunks)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_docs = text_splitter.split_documents(documents=docs)
print(split_docs)

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key = "OPENAI_API_KEY",
)