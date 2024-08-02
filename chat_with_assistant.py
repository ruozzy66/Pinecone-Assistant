import sys
import json
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def chat_with_assistant(api_key, assistant_name, messages):
    pc = Pinecone(api_key=api_key)
    assistant = pc.assistant.describe_assistant(assistant_name)
    
    chat_context = [Message(**msg) for msg in json.loads(messages)]
    response = assistant.chat_completions(messages=chat_context)
    
    # Convert the response to a serializable format
    serializable_response = {
        "id": response.id,
        "choices": [{
            "message": {
                "role": choice.message.role,
                "content": choice.message.content
            },
            "finish_reason": choice.finish_reason,
            "index": choice.index
        } for choice in response.choices],
        "model": response.model
    }
    
    return json.dumps(serializable_response)

if __name__ == "__main__":
    api_key = sys.argv[1]
    assistant_name = sys.argv[2]
    messages = sys.argv[3]
    
    result = chat_with_assistant(api_key, assistant_name, messages)
    print(result)