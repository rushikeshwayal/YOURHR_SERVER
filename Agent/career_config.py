# Agent/config.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, PydanticOutputParser
from langchain.utilities import SerpAPIWrapper
import re
import json
from dotenv import load_dotenv

load_dotenv()


class CustomAgentWithSearch:

    def __init__(self, serpapi_key: str = None):
        print("CareerPath Agent Initialized ✅")

        # Supported LLM models
        self.models = {
            "google": ChatGoogleGenerativeAI,
            "openai": ChatOpenAI
        }

        # Output parsers
        self.output_parsers = {
            "str": StrOutputParser,
            "json": JsonOutputParser,
            "pydantic": PydanticOutputParser
        }

        # Optional search tool
        self.tools = []
        if serpapi_key:
            self.search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
            self.tools.append(
                Tool(
                    name="Search",
                    func=self.search.run,
                    description="Use this tool to search the internet for up-to-date resources, courses, tutorials, or documentation."
                )
            )

    def invoke_agent(
        self,
        system_input: str,
        user_input: str,
        model_name: str = "google",
        model_variant: str = "gemini-2.5-flash", # Updated model for better performance
        output_parser: str = "json",
        use_tools: bool = False
    ):
        if model_name not in self.models:
            raise ValueError(f"Invalid model '{model_name}'. Available models: {list(self.models.keys())}")

        llm = self.models[model_name](model=model_variant)

        if use_tools and self.tools:
            # Initialize a React agent with tools
            # IMPORTANT: The user_input for a ReAct agent should explicitly ask for the 'Final Answer:' format.
            # Example modification in your router: f"{original_prompt}\n\n...When you have the final answer, prefix it with 'Final Answer:'."
            agent = initialize_agent(
                tools=self.tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True, # This helps but doesn't guarantee clean output
            )
            raw_output = agent.run(user_input)
            
            # ✨ FIX: Extract JSON from the agent's potentially messy output string.
            # This regex looks for a string starting with '[' and ending with ']' or starting with '{' and ending with '}'.
            json_match = re.search(r'\[.*\]|\{.*\}', raw_output, re.DOTALL)
            if json_match:
                cleaned_output = json_match.group(0)
            else:
                # If no JSON is found, the agent failed. Raise a clear error.
                raise ValueError(f"Agent did not return a parsable JSON object. Raw output: '{raw_output}'")

        else:
            # Static prompt only
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_input),
                ("user", user_input),
            ])
            formatted_prompt = prompt_template.format()
            raw_output = llm.invoke(formatted_prompt).content
            # Clean potential markdown code blocks from direct LLM output
            cleaned_output = re.sub(r"^```json+|```+$", "", raw_output.strip())
 
        # ✨ FIX: Use a robust try-except block for JSON parsing.
        try:
            # The output parser selection logic is now simplified
            if output_parser == 'json':
                parsed_output = json.loads(cleaned_output)
            elif output_parser == 'str':
                parser = StrOutputParser()
                parsed_output = parser.parse(cleaned_output)
            # Add other parsers like Pydantic here if needed
            else:
                parsed_output = cleaned_output # Default to returning the cleaned string

            return parsed_output

        except json.JSONDecodeError as e:
            # Provide a much more informative error if JSON parsing fails
            error_message = f"Failed to decode JSON. Error: {e}. Cleaned output that caused the error was: '{cleaned_output}'"
            raise ValueError(error_message) from e


    def model_list(self):
        return list(self.models.keys())

    def output_parser_list(self):
        return list(self.output_parsers.keys())