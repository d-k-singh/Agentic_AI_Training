#Import ADK components and Gemini LLM
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
import asyncio
print("✅ ADK components imported successfully.")

#Configure Retry Options
#When working with LLMs, you may encounter transient errors like rate limits or temporary service unavailability. Retry options automatically handle these failures by retrying the request with exponential backoff.
retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

#Define your agent
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

print("✅ Root Agent defined.")

#Run your agent
#Create an InMemoryRunner and tell it to use our root_agent
runner = InMemoryRunner(agent=root_agent)
print("✅ Runner created.")

#Now you can call the .run_debug() method to send our prompt and get an answer.
#This method abstracts the process of session creation and maintenance and is used in prototyping
#response = await runner.run_debug(
#   "What is Agent Development Kit from Google? What languages is the SDK available in?"
#)

import os
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not set")

async def main():
    response = await runner.run_debug(
        "What is Agent Development Kit from Google? What languages is the SDK available in?"
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())

#Run the command below to generate a sample-agent folder that contains all the necessary files, 
# including agent.py for your code, an .env file with your API key pre-configured, and an __init__.py file
#adk create sample-agent --model gemini-2.5-flash-lite --api_key $GOOGLE_API_KEY

#Get your custom URL to access the ADK web UI in the Kaggle Notebooks environment:
#url_prefix = get_adk_proxy_url()

#Now we can run ADK web:
#adk web --url_prefix {url_prefix}