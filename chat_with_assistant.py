import sys
import json
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def remove_after_references(text):
    """Remove everything after the word 'References' including it."""
    ref_index = text.find('References')
    if (ref_index != -1):
        return text[:ref_index].strip()
    return text

def chat_with_assistant(api_key, assistant_name, messages):
    try:
        print("Connecting to Pinecone")
        pc = Pinecone(api_key=api_key)
        assistant = pc.assistant.describe_assistant(assistant_name)
        
        print("Processing messages:", messages)
        chat_context = [Message(**msg) for msg in json.loads(messages)]
        response = assistant.chat_completions(messages=chat_context)
        
        # Remove everything after 'References'
        for choice in response.choices:
            choice.message.content = remove_after_references(choice.message.content)
        
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
        
        print("Response generated:", serializable_response)
        return json.dumps(serializable_response)
    
    except Exception as e:
        print("Error occurred:", e)
        return json.dumps({
            "error": "An error occurred during the assistant interaction.",
            "details": str(e)
        })

if __name__ == "__main__":
    api_key = sys.argv[1]
    assistant_name = sys.argv[2]
    messages = sys.argv[3]
    
    result = chat_with_assistant(api_key, assistant_name, messages)
    print(result)
