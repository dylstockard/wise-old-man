import os
import yaml

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo


# Load the system prompts
PROMPTS_PATH = "prompts.yaml"


class ChatBot:
    """The chat bot"""

    def __init__(self) -> None:
        """Initializes the chat bot"""
        self.prompts = self.load_prompts()
        self.model = ChatOpenAI(model=os.getenv("DEPLOYMENT_NAME"), seed=36)
        self.memory = ChatMessageHistory()

    def load_prompts(self) -> dict:
        """Loads prompts from a YAML file."""
        with open(PROMPTS_PATH, "r") as file:
            return yaml.safe_load(file)

    def answer(
        self, query: str, character: str = "", token_limit: int = 20
    ) -> ChatPromptTemplate:
        """"""
        # Define the output parser
        parser = StrOutputParser()

        # Define the prompt template
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.prompts["system_prompt"]),
                ("placeholder", "{chat_history}"),
                ("user", "{query}"),
            ]
        )

        # Create a chain with memory
        chain = prompt_template | self.model | parser

        chain_with_message_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: self.memory,
            input_messages_key="query",
            history_messages_key="chat_history",
        )

        # Invoke the chain
        ans = chain_with_message_history.invoke(
            {"query": query, "character": character, "tokens": token_limit},
            {"configurable": {"session_id": "memory"}},
        )

        return ans

    def answer_from_html(
        self,
        query: str,
        path_to_html: str = "webpages",
        character: str = "",
        token_limit: int = 20,
    ) -> ChatPromptTemplate:

        # Retrieval fields
        persist_directory = "chroma/"
        embedding = OpenAIEmbeddings()
        vectordb = Chroma(
            persist_directory=persist_directory, embedding_function=embedding
        )

        # Load the html page(s) into the Chroma db
        for page_html in os.listdir(path_to_html):
            full_page_html_path = os.path.join(path_to_html, page_html)
            loader = UnstructuredHTMLLoader(full_page_html_path)
            data = loader.load()
            vectordb.add_documents(documents=data, embedding=embedding)

        # Define necessary info for Query retriever
        metadata_field_info = [
            AttributeInfo(
                name="source",
                description="The name of the html file the data is from",
                type="string",
            )
        ]
        document_content_description = "OSRS Wiki Pages"

        # Define the Query retriever
        retriever = SelfQueryRetriever.from_llm(
            self.model,
            vectordb,
            document_content_description,
            metadata_field_info,
            verbose=True,
        )

        # invoke the retriever
        docs = retriever.invoke(query)
        return docs[0].metadata
