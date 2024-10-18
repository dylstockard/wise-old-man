import os
import yaml

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load the system prompts
PROMPTS_PATH = "prompts.yaml"


class ChatBot:
    """The chat bot"""

    def __init__(self) -> None:
        """Initializes the chat bot"""
        self.prompts = self.load_prompts()
        self.model = ChatOpenAI(model=os.getenv("DEPLOYMENT_NAME"), seed=36)

    def load_prompts(self) -> dict:
        """Loads prompts from a YAML file."""
        with open(PROMPTS_PATH, "r") as file:
            return yaml.safe_load(file)

    def answer(self, query:str, character:str="", token_limit:int=100) -> ChatPromptTemplate:
        """"""
        # Define the output parser
        parser = StrOutputParser()

        # Define the prompt template
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.prompts["system_prompt"]), ("user", query)]
        )

        # Adjust the prompt for the user input
        final_prompt = prompt_template.invoke(
            {"character": character, "tokens": token_limit}
        )
        
        # Create a chain
        chain = prompt_template | self.model | parser

        # Invoke the chain
        ans = chain.invoke(
            {"character": character, "tokens": token_limit}
        )

        return ans
