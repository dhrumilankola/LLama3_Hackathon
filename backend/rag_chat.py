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

class ConversationalRAG:
    def __init__(
        self,
        document_dir: str,
        embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
        generative_model: str = "meta-llama/Llama-3-8b-chat-hf"
    ):
        self.service_context = ServiceContext.from_defaults(
        llm=TogetherLLM(
            generative_model,
            temperature=0.8,
            max_tokens=512,  # Increase this value
            top_p=0.7,
            top_k=50,
            is_chat_model=True,  # Change this to True if using a chat model
            completion_to_prompt=completion_to_prompt
        ),
            embed_model=TogetherEmbedding(embedding_model, api_key=api_key)
        )
        
        documents = SimpleDirectoryReader(document_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents, service_context=self.service_context)
        self.chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=self.index.as_query_engine(similarity_top_k=5),
            service_context=self.service_context,
            verbose=True
        )
        self.chat_history: List[ChatMessage] = []

    def chat(self, query: str) -> str:
        response = self.chat_engine.chat(query, chat_history=self.chat_history)
        self.chat_history.append(ChatMessage(role='user', content=query))
        self.chat_history.append(ChatMessage(role='assistant', content=str(response)))
        return str(response)
    

    def clear_history(self):
        self.chat_history.clear()
