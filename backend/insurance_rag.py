import os
from typing import List
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, Document
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.base.llms.types import ChatMessage

load_dotenv()
api_key = os.getenv('TOGETHER_API_KEY')

def completion_to_prompt(completion: str) -> str:
    return f"{completion}"

class InsuranceRAG:
    def __init__(
        self,
        insurance_type: str,
        document_dir: str = "./docs",
        embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
        generative_model: str = "meta-llama/Llama-3-8b-chat-hf"
    ):
        self.insurance_type = insurance_type
        self.document_dir = os.path.join(document_dir, insurance_type)
        self.service_context = ServiceContext.from_defaults(
            llm=TogetherLLM(
                generative_model,
                temperature=0.8,
                max_tokens=512,
                top_p=0.7,
                top_k=50,
                is_chat_model=True,
                completion_to_prompt=completion_to_prompt
            ),
            embed_model=TogetherEmbedding(embedding_model, api_key=api_key)
        )
        
        self.index = self.load_documents()
        self.chat_engine = self.create_chat_engine()
        self.chat_history: List[ChatMessage] = []

    def load_documents(self):
        if self.insurance_type == 'custom':
            return VectorStoreIndex([], service_context=self.service_context)
        else:
            documents = SimpleDirectoryReader(self.document_dir).load_data()
            return VectorStoreIndex.from_documents(documents, service_context=self.service_context)
        
    def add_document(self, file_path: str):
        if self.insurance_type == 'custom':
            try:
                documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
                if isinstance(documents, list):
                    for doc in documents:
                        self.index.insert(doc)
                else:
                    self.index.insert(documents)
                self.chat_engine = self.create_chat_engine()
                print(f"Document added successfully: {file_path}")
            except Exception as e:
                print(f"Error adding document: {str(e)}")
                raise

    def create_chat_engine(self):
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.index.as_query_engine(similarity_top_k=5),
            service_context=self.service_context,
            verbose=True
        )

    def chat(self, query: str) -> str:
        response = self.chat_engine.chat(query, chat_history=self.chat_history)
        self.chat_history.append(ChatMessage(role='user', content=query))
        self.chat_history.append(ChatMessage(role='assistant', content=str(response)))
        return str(response)

    def clear_history(self):
        self.chat_history.clear()

def add_document(self, file_path: str):
    if self.insurance_type == 'custom':
        try:
            documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
            if isinstance(documents, list):
                for doc in documents:
                    self.index.insert(doc)
            else:
                self.index.insert(documents)
            self.chat_engine = self.create_chat_engine()
            print(f"Document added successfully: {file_path}")
        except Exception as e:
            print(f"Error adding document: {str(e)}")
            raise

    def remove_all_documents(self):
        if self.insurance_type == 'custom':
            self.index = VectorStoreIndex([], service_context=self.service_context)
            self.chat_engine = self.create_chat_engine()
            self.clear_history()