import chromadb
import os
from commons import ENV_PORT_CHROMADB, ENV_SERVER_CHROMADB

# ENV CONFIG CRHOMA
HOST_CHROMADB = os.getenv(ENV_SERVER_CHROMADB, "0.0.0.0")
PORT_CHROMADB = int(os.getenv(ENV_PORT_CHROMADB, 8081))

_chroma_client = chromadb.HttpClient(
    host=HOST_CHROMADB,
    port=PORT_CHROMADB,
)

def create_chromadb_collection(name, metadata):
    collection = _chroma_client.create_collection(
        name,
        metadata=metadata,
    )
    return collection

def chormadb_insert_data(collection, ids, content, embeddings):
    collection.add(documents=content, ids=ids, embeddings=embeddings)