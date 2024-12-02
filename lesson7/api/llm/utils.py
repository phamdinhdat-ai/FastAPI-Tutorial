import os
import json 
import logging 
import pathlib
from pathlib import Path
import yaml
from typing import Any, Dict, List, Tuple
from docling.document_converter import DocumentConverter, PdfFormatOption, WordFormatOption

from docling.datamodel.base_models import InputFormat
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling_core.transforms.chunker.hierarchical_chunker import HierarchicalChunker
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

import typing 
from typing import Iterator, List
from langchain_core.document_loaders import  BaseLoader 
from langchain_core.documents import Document
from docling.document_converter import DocumentConverter

class DocumentPDFLoader(BaseLoader):
    
    def __init__(self, filepath: List[str]) -> None: 
        self._filepath = filepath if isinstance(filepath, list) else [filepath]
        self._coverter = DocumentConverter()
    
    def lazy_load (self)->Iterator[Document]:
        for file in self._filepath:
            dl = self._coverter.convert(file).document
            text = dl.export_to_markdown()
            yield Document(page_content=text)

class DocumentCustomConverter(BaseLoader):
        
        def __init__(self, filepath: List[str], type_doc:str = 'markdown') -> None: 
            self._filepath = filepath if isinstance(filepath, list) else [filepath]
            self._type_doc = type_doc
            self.pipeline_options = PdfPipelineOptions()
            self.pipeline_options.do_ocr = False 
            self.pipeline_options.do_table_structure = True 
            self.document_coverter = (
                DocumentConverter(
                    allowed_formats=[
                        InputFormat.PDF,
                        InputFormat.DOCX,
                        InputFormat.HTML,
                        InputFormat.PPTX, 
                        InputFormat.XLSX
                    ], 
                    format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=self.pipeline_options,
                                                                    backend=PyPdfiumDocumentBackend), 
                                    InputFormat.DOCX: WordFormatOption(pipeline_cls = SimplePipeline)} 
                )
            )
            
        def lazy_load(self) -> Iterator[Document]:
            for file in self._filepath:
                coverted_docment  = self.document_coverter.convert(file , raises_on_error=False)
                if self._type_doc == 'markdown':
                    yield Document(page_content=coverted_docment.document.export_to_markdown())
                else:
                    yield Document(page_content=coverted_docment.document.export_to_dict())


def covert_document(file_path:str, type_doc:str = 'markdown'):
    
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False 
    pipeline_options.do_table_structure = True 
    document_coverter = (
        DocumentConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.DOCX,
                InputFormat.HTML,
                InputFormat.PPTX, 
                InputFormat.XLSX
            ], 
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options,
                                                             backend=PyPdfiumDocumentBackend), 
                            InputFormat.DOCX: WordFormatOption(pipeline_cls = SimplePipeline)} 
        )
    )
    
    coverted_docment  = document_coverter.convert(file_path , raises_on_error=False)
    if type_doc == 'markdown':
        return coverted_docment.document.export_to_markdown()
    else:
        return coverted_docment.document.export_to_dict()
    
    
    
    
def document_chunking(docs : List[str], chunker) -> List[str]:
    text_chunks  = chunker.split_documents(docs)
    return text_chunks


def create_vectorstore(text_chunks:List[str], embeddings) -> Any:
    return FAISS.from_documents(text_chunks, embedding=embeddings)

def load_embeddings(embedding_path:str): # loadd embeddings from huggingface
    embdding = HuggingFaceEmbeddings(model_name = embedding_path)
    return embdding

def load_model(model_hf_path: str, hf_api_token:str):
    llm = HuggingFaceEndpoint(
        repo_id=model_hf_path,
        huggingfacehub_api_token=hf_api_token
        
    )
    return llm