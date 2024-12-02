import os 
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from utils import document_chunking, load_embeddings, load_model, create_vectorstore, DocumentCustomConverter

# lesson7\api\llm\document_data\s10586-022-03658-4.pdf
file_path = './document_data/s10586-022-03658-4.pdf'
HF_EMBEDDING = "BAAI/bge-small-en-v1.5"
HF_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = "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"


covert_document = DocumentCustomConverter([file_path], type_doc='markdown')
# loader = DocumentPDFLoader([file_path])
chunker = RecursiveCharacterTextSplitter(chunk_size=512 ,  chunk_overlap=100)
print("="*100)
print("Converting document")
results = covert_document.load()
print("="*100)
print("Chunking document")
chunks = document_chunking(results, chunker)
print("="*100)
embedding = load_embeddings(HF_EMBEDDING)
print("Load Embeddings")
print("="*100)
vectorstores = create_vectorstore(text_chunks=chunks, embeddings=embedding)
print("Create Vectorstore")

print("="*100)
print("Invorking data")
question_1 = "How many pages were human annotated for DocLayNet?"
question_2 = "What is the performance of MRCNN model in class Caption with metrics mAP@0.5-0.95 ?"
print("Question1: ", question_1)
results = vectorstores.similarity_search_with_score(question_1, k = 3)
for res, score in results:
    print(f"* [SIM = {score:.2f}] | [{res.page_content}]")
print("="*100)

print("Question2: ", question_2)
results = vectorstores.similarity_search_with_score(question_2, k = 3)
for res, score in results:
    print(f"* [SIM = {score:.2f}] | [{res.page_content}]")
print("="*100)
llm = load_model(model_hf_path=HF_REPO_ID, hf_api_token=HF_TOKEN)