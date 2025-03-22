import uuid
from langchain_google_vertexai import VertexAIEmbeddings


def generate_documents(documents):
    ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in documents]
    unique_ids = list(set(ids))
    new_embeddings = []
    new_content = []

    for doc in documents:
        new_embeddings.append(VertexAIEmbeddings().embed_query(doc.page_content))
        new_content.append(doc.page_content)

    return unique_ids, new_content, new_embeddings
