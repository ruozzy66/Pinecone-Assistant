import sys
import json
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def remove_after_references(text):
    """Remove everything after the word 'References' including it."""
    ref_index = text.find('References')
    if ref_index != -1:
        return text[:ref_index].strip()
    return text

def format_response(text):
    """Format the response with bullet points and appropriate formatting."""
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        # Replace ** with <b> HTML tags for bold text
        while '**' in line:
            line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
        
        # Ensure the bullet points are correctly formatted
        if line.strip():
            if line[0].isdigit() and (line[1] == '.' or line[2] == '.'):
                formatted_lines.append(f'<li>{line.strip()}</li>')
            else:
                formatted_lines.append(line)
    
    return '<ul>' + '\n'.join(formatted_lines) + '</ul>'

def chat_with_assistant(api_key, assistant_name, messages):
    try:
        pc = Pinecone(api_key=api_key)
        assistant = pc.assistant.describe_assistant(assistant_name)
        
        chat_context = [Message(**msg) for msg in json.loads(messages)]
        response = assistant.chat_completions(messages=chat_context)
        
        # Remove everything after 'References' and format the response
        #for choice in response.choices:
        #    choice.message.content = format_response(remove_after_references(choice.message.content))
        
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
    
    except Exception as e:
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
