from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message



pc = Pinecone(api_key="7864d99d-5ee4-4ab2-b615-b9173ec27ce1")

# Get your assistant.
assistant = pc.assistant.describe_assistant("ti4-rules-assistant")

# Chat with the Assistant.
chat_context = [Message(content='how many action cards in twilight imperium 4?')]
response = assistant.chat_completions(messages=chat_context)
