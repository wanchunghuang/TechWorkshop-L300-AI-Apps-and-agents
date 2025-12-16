import os
import sys

# Load .env BEFORE any other imports
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(env_path)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ToolSet
from agent_processor import create_function_tool_for_agent
from agent_initializer import initialize_agent

CM_PROMPT_TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'prompts', 'CartManagerPrompt.txt')
with open(CM_PROMPT_TARGET, 'r', encoding='utf-8') as file:
    CM_PROMPT = file.read()

project_endpoint = os.environ["AZURE_AI_AGENT_ENDPOINT"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

# Create function tools for cart manager agent
functions = create_function_tool_for_agent("cart_manager")
toolset = ToolSet()
toolset.add(functions)
project_client.agents.enable_auto_function_calls(tools=functions)

initialize_agent(
    project_client=project_client,
    model=os.environ["AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME"],
    env_var_name="cart_manager",
    name="Zava Cart Manager Agent",
    instructions=CM_PROMPT,
    toolset=toolset
)
