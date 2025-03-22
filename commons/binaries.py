from PyPDF2 import PdfReader, PdfWriter
from commons import ocr
import tempfile, shutil, os
import ntpath

from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

tmp_dir = tempfile.gettempdir()


def path_leaf(path):
    """
    Extrae el nombre del archivo de una ruta dada.
    Args:
        path (str): La ruta completa del archivo.
    Returns:
        str: El nombre del archivo extraído de la ruta.
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def prepare_dir(path):
    """
    Prepara un directorio de trabajo temporal para un archivo dado.

    Args:
        path (str): La ruta completa del archivo original.

    Returns:
        tuple: Una tupla que contiene la ruta del directorio de trabajo temporal y el nombre del archivo.

    Funcionalidad:
        - Obtiene el nombre del archivo sin espacios.
        - Crea un directorio temporal basado en el nombre del archivo.
        - Elimina el directorio temporal si ya existe.
        - Crea un nuevo directorio temporal.
        - Copia el archivo original al nuevo directorio temporal.

    Excepciones:
        - Si el directorio temporal no existe, imprime un mensaje indicando que el directorio no existe.
    """
    # Obtenemos el nombre del archivo sin espacios
    fname = path_leaf(path).replace(" ", "_")
    sname = os.path.splitext(fname)[0]
    work_dir = tmp_dir + "/" + sname

    try:
        shutil.rmtree(work_dir)
    except:
        print("El directorio no existe.")

    os.mkdir(work_dir)
    new_path = work_dir + "/" + fname
    shutil.copyfile(path, new_path)
    return work_dir, fname


def split_pdf(path, work_dir, fname):
    """
    Divide un archivo PDF en páginas individuales y guarda cada página como un archivo PDF separado.

    Args:
        path (str): La ruta del archivo PDF de entrada.
        work_dir (str): El directorio de trabajo donde se guardarán los archivos PDF resultantes.
        fname (str): El nombre base para los archivos PDF resultantes.

    Returns:
        list: Una lista de rutas de los archivos PDF generados, cada uno correspondiente a una página del PDF original.
    """
    pdf = PdfReader(open(path, "rb"))
    pages = []

    for page in range(len(pdf.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])

        output_filename = "{}/{}_page_{}.pdf".format(work_dir, fname, page + 1)

        with open(output_filename, "wb") as out:
            pdf_writer.write(out)

        pages.append(output_filename)

    return pages


def create_file(path, file_name, content_type="text/plain", content=None):
    """
    Crea un archivo en la ruta especificada con el nombre y contenido dados.

    Args:
        path (str): La ruta donde se creará el archivo.
        file_name (str): El nombre del archivo a crear.
        content_type (str, opcional): El tipo de contenido del archivo. Por defecto es "text/plain".
        content (str, opcional): El contenido a escribir en el archivo. Por defecto es None.

    Returns:
        str: La ruta completa del archivo creado.
    """
    ocr_file = path + "/" + file_name + ".txt"
    f = open(ocr_file, "a")
    f.write(content)
    f.close
    return ocr_file


def count_token(content):
    tokenizer = Tokenizer.from_file("./gpt2_tokenizer/tokenizer.json")
    output = tokenizer.encode(content)

    return len(output.ids)


def process_document(path: str):
    work_dir, fname = prepare_dir(path)
    # Dividimos el documento pdf en páginas para no tener problemas con el OCR
    pages = split_pdf(path, work_dir, fname)

    # Nombre del archivo sin extensión
    sname = os.path.splitext(fname)[0]

    current_content = ""
    # Realizamos el ocr de cada una de las páginas
    for page in pages:
        content = ocr.process_documents(
            project_id=os.getenv("project_id"),
            location=os.getenv("location"),
            processor_id=os.getenv("processor_ocr_id"),
            processor_version_id=os.getenv("processor_ocr_version"),
            input_mime_type="application/pdf",
            document=page,
        )

        current_content += content

    # contamos el número de tokens
    token = count_token(current_content)
    # dividimos el texto en secciones para poder generar los emedings
    loader = UnstructuredFileLoader(ocr_file)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

    docs = text_splitter.split_documents(documents)

    ocr_file = create_file(work_dir, sname, content=current_content)

    metadata = {
        "token": token,
        "num_docs": len(docs),
        "doc_name": sname,
    }
    collection = create_chromadb_collection(sname, metadata)

    ids, new_content, new_embeddings = generate_documents(docs, embeddings_engine)

    print("Insertamos los documentos en la base de datos de chromadb.")
    chormadb_insert_data(collection, ids, new_content, new_embeddings)
