import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")
model_name = os.getenv("GEMINI_MODEL_NAME")

if not all([api_key, base_url, model_name]):
    raise ValueError("Missing Gemini configuration in .env file")


client = AsyncOpenAI(api_key=api_key, base_url=base_url)

set_tracing_disabled(True)
set_default_openai_client(client, use_for_tracing=False)


model = OpenAIChatCompletionsModel(model=model_name, openai_client=client)
