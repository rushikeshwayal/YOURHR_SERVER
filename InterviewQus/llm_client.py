# InterviewQus/llm_client.py
from langchain_google_genai import ChatGoogleGenerativeAI
from InterviewQus.prompts import Prompts
from pyserver.Agent.config import CustomAgent
from dotenv import load_dotenv

load_dotenv()

prompt = Prompts()
agent = CustomAgent()



user_input = prompt.user_prompt(
    job_title="{title}",
    company_name="{company_name}",
    skills_required="{skills}",
    experience_required="{experience}",
    job_description="{description}"
)

response = agent.invoke_agent(
    system_input=prompt.system_prompt(),
    user_input=user_input,
    model_name="google",
    model_variant="gemini-2.5-flash"
)


