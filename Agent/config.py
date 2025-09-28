from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, PydanticOutputParser
from dotenv import load_dotenv

load_dotenv()


class CustomAgent:

    def __init__(self):
        print("Vertical Agent Initialized✅")
        self.models = {
            "google": ChatGoogleGenerativeAI,
            "openai": ChatOpenAI
        }
        self.output_parsers = {
            "str": StrOutputParser,
            "json": JsonOutputParser,
            "pydantic": PydanticOutputParser
        }

    def invoke_agent(
        self,
        system_input: str,
        user_input: str,
        model_name: str,
        model_variant: str,
        output_parser: str = "json",
    ):
        if model_name not in self.models:
            raise ValueError(f"Invalid model '{model_name}'. Available models: {list(self.models.keys())}")

        llm = self.models[model_name](model=model_variant)

        # Prompt template (system + user)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_input),
            ("user", user_input),
        ])

        # format prompt into messages
        formatted_prompt = prompt_template.format()

        # directly invoke the model (NO agent)
        raw_output = llm.invoke(formatted_prompt)

        # parse the output
        parser_cls = self.output_parsers[output_parser]
        parser = parser_cls()

        # .content contains the actual text from the LLM
        parsed_output = parser.parse(raw_output.content)

        return parsed_output

    def model_list(self):
        return list(self.models.keys())

    def output_parser_list(self):
        return list(self.output_parsers.keys())
