import os
from typing import List
from dotenv import load_dotenv
from llama_index.core import ServiceContext, VectorStoreIndex, Document
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.base.llms.types import ChatMessage
import pdfplumber

load_dotenv()
api_key = os.getenv('TOGETHER_API_KEY')

def completion_to_prompt(completion: str) -> str:
    system_prompt = """You are an AI assistant designed to help students answer questions based on provided documents. 
    Your responses should be:
    1. Accurate and based solely on the information in the documents.
    2. Clear and easy for students to understand.
    3. Concise but comprehensive.
    4. Focused on addressing the specific question asked.

    If the information to answer a question is not in the documents, say "I'm sorry, but I don't have enough information in the provided documents to answer that question accurately." 
    Do not make up or infer information that isn't explicitly stated in the documents.

    If appropriate, you can suggest related topics from the documents that the student might find helpful or interesting.

    Remember, your goal is to assist students in learning and understanding the material, not to provide answers that aren't supported by the documents."""

    return f"<s>[INST] {system_prompt}\n\nHuman: {completion} [/INST]\n\nAssistant: </s>"

def extract_text_from_pdf(pdf_path: str) -> str:
    text_content = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_content.append(page.extract_text())
            tables = page.extract_tables()
            for table in tables:
                if table:
                    table_text = "\n".join([" | ".join(map(str, row)) for row in table])
                    text_content.append(table_text)
    return "\n".join(text_content)

class SimpleTableDirectoryReader:
    def __init__(self, directory: str):
        self.directory = directory

    def load_data(self) -> List[Document]:
        documents = []
        for file_name in os.listdir(self.directory):
            if file_name.endswith('.pdf'):
                file_path = os.path.join(self.directory, file_name)
                text = extract_text_from_pdf(file_path)
                documents.append(Document(text=text))
        return documents

class ConversationalRAG:
    def __init__(
        self,
        document_dir: str,
        embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
        generative_model: str = "meta-llama/Meta-Llama-3-70B-Instruct-Turbo"
    ):
        self.service_context = ServiceContext.from_defaults(
            llm=TogetherLLM(
                generative_model,
                temperature=0.8,
                max_tokens=256,
                top_p=0.7,
                top_k=50,
                is_chat_model=False,
                completion_to_prompt=completion_to_prompt
            ),
            embed_model=TogetherEmbedding(embedding_model, api_key=api_key)
        )
        
        documents = SimpleTableDirectoryReader(document_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents, service_context=self.service_context)
        self.chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=self.index.as_query_engine(similarity_top_k=25),
            service_context=self.service_context,
            verbose=True
        )
        self.chat_history: List[ChatMessage] = []

    def chat(self, query: str) -> str:
        response = self.chat_engine.chat(query, chat_history=self.chat_history)
        self.chat_history.append(ChatMessage(role='user', content=query))
        self.chat_history.append(ChatMessage(role='assistant', content=str(response)))
        return str(response)

# Usage
document_dir = "./docs"
rag = ConversationalRAG(document_dir)

while True:
    query = input("You: ")
    if query.lower() in ['exit', 'quit', 'bye']:
        print("Goodbye!")
        break
    response = rag.chat(query)
    print(f"AI: {response}")