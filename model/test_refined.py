import os
from typing import List, Tuple
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, Document
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.base.llms.types import ChatMessage

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

class ConversationalRAG:
    def __init__(
        self,
        document_dir: str,
        embedding_model: str = "togethercomputer/m2-bert-80M-8k-retrieval",
        generative_model: str = "meta-llama/Llama-2-70b-chat-hf"
    ):
        self.service_context = ServiceContext.from_defaults(
            llm=TogetherLLM(
                generative_model,
                temperature=0.7,  # Slightly reduced for more focused responses
                max_tokens=512,   # Increased to allow for more comprehensive answers
                top_p=0.9,
                top_k=50,
                is_chat_model=True,
                completion_to_prompt=completion_to_prompt
            ),
            embed_model=TogetherEmbedding(embedding_model, api_key=api_key)
        )
        
        documents = SimpleDirectoryReader(document_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents, service_context=self.service_context)
        self.chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=self.index.as_query_engine(similarity_top_k=3),  # Reduced to focus on most relevant docs
            service_context=self.service_context,
            verbose=True,
            condense_question_prompt=(
                "Given the following conversation history and a new question, rephrase the new question to be a standalone question that captures all necessary context from the conversation history.\n"
                "Chat History:\n{chat_history}\n"
                "New Question: {question}\n"
                "Standalone question:"
            )
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

print("Welcome to the Student Assistant AI. Ask questions about the provided documents, or type 'exit' to quit.")

while True:
    query = input("You: ")
    if query.lower() in ['exit', 'quit', 'bye']:
        print("Thank you for using the Student Assistant AI. Goodbye!")
        break
    response = rag.chat(query)
    print(f"AI: {response}")