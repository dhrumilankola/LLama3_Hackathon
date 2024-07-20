import os
from typing import List, Tuple
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, Document
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core import Settings
load_dotenv()
api_key = os.getenv('TOGETHER_API_KEY')

def completion_to_prompt(completion: str) -> str:
    return f"<s>[INST] {completion} [/INST] </s>\n"

class ConversationalRAG:
    def __init__(
        self,
        document_dir: str,
        embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
        generative_model: str = "meta-llama/Llama-3-8b-chat-hf"
    ):
        Settings.llm = TogetherLLM(
            generative_model,
            temperature=0.7,
            max_tokens=512,
            top_p=0.9,
            api_key=api_key,
            is_chat_model=False,
            completion_to_prompt=completion_to_prompt
        )
        Settings.embed_model = TogetherEmbedding(embedding_model, api_key=api_key)
        
        documents = SimpleDirectoryReader(document_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents)
        self.chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=self.index.as_query_engine(similarity_top_k=3),
            verbose=True
        )
        self.chat_history: List[ChatMessage] = []

    def chat(self, query: str) -> str:
        response = self.chat_engine.chat(query, chat_history=self.chat_history)
        self.chat_history.append(ChatMessage(role='user', content=query))
        self.chat_history.append(ChatMessage(role='assistant', content=str(response)))
        
        # Extract only the relevant part of the response
        response_str = str(response)
        if "[INST]" in response_str:
            response_str = response_str.split("[INST]")[-1]
        if "[/INST]" in response_str:
            response_str = response_str.split("[/INST]")[0]
        
        return response_str.strip()

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