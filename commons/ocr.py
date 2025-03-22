import os

import google.cloud.logging
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud.documentai_toolbox import document as documentai_document_wrapper


log_client = google.cloud.logging.Client(project=os.getenv("project_id"))
log_client.setup_logging()

log_name = "genai-vertex-unstructured-log"
logger = log_client.logger(log_name)


def process_documents(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version_id: str = None,
    input_mime_type: str = None,
    document: str = None,
):
    # You must set the api_endpoint if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if processor_version_id:
        resource_name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:
        resource_name = client.processor_path(project_id, location, processor_id)

    # storage_client = storage.Client()
    # bucket = storage_client.bucket(bucket_name)
    # blob = bucket.blob(document.replace(f"{bucket_name}/", ""))
    with open(document, "rb") as image_file:
        image_content = image_file.read()
    # image_content = read_file(bucket_name, document.replace(f"{bucket_name}/", ""))

    raw_document = documentai.RawDocument(
        content=image_content, mime_type=input_mime_type
    )

    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    # Use the Document AI client to process the sample form
    result = client.process_document(request=request)

    wrapped_document = documentai_document_wrapper.Document.from_documentai_document(
        documentai_document=result.document
    )

    return wrapped_document.text
