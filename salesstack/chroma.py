from chroma_haystack import ChromaDocumentStore
from haystack.preview.components.file_converters import TextFileToDocument
from haystack.preview.components.writers import DocumentWriter

PATH_TO_FILES=["../catalogue/sample.txt"]

def init_document_store():
    document_store = ChromaDocumentStore()
    indexing = Pipeline()
    indexing.add_component("converter", TextFileToDocument())
    indexing.add_component("writer", DocumentWriter(document_store))
    indexing.connect("converter", "writer")
    indexing.run({"converter":{"paths":PATH_TO_FILES}})
    return ChromaDocumentStore()
