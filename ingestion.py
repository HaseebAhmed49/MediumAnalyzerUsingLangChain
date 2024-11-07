import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient, ServerlessSpec

load_dotenv()

if __name__ == '__main__':
    print("Ingesting..")

    loader = TextLoader("/Users/haseebahmed/Desktop/LLM/intro-to-vector-dbs/mediumblog1.txt")
    document = loader.load();

    print("Splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    # Set up Pinecone instance
    pc = PineconeClient(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

    # Create or connect to the index
    index_name = os.environ["INDEX_NAME"]
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # Update this to match your embeddings dimension
            metric='cosine', # or 'euclidean', depending on your needs
            spec=ServerlessSpec(
                cloud='aws',     # Adjust to your preferred cloud provider
                region='us-east-2'  # Adjust to the preferred region
            )
        )

    print("ingesting..")

    Pinecone.from_documents(texts, embeddings, index_name=os.environ["INDEX_NAME"])