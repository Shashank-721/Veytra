# This module will contain Veytra's LLM configuration.
# The model will be accessed through the Hugging Face Inference API.

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace


# Load variables from the .env file.
load_dotenv()


# Create the Hugging Face endpoint.
# The actual API token is read from the environment.
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
)


# Wrap the Hugging Face endpoint as a chat model.
# This gives us the interface we will later use
# with LangChain and LangGraph.
model = ChatHuggingFace(llm=llm)

# Test the model when this file is executed directly.
if __name__ == "__main__":

    # Send a simple message to the model.
    response = model.invoke("What is a production incident?")

    # Print the model's response.
    print(response.content)