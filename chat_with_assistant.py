import sys
import json
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def format_references(text):
    """Format the references section by making text name clickable and hiding URL."""
    if 'References' not in text:
        return text
    
    parts = text.split('References')
    main_text = parts[0]
    references_text = parts[1]
    
    formatted_references = []
    for line in references_text.split('\n'):
        if '[' in line and ']' in line and '(' in line and ')' in line:
            ref_number = line.split('[')[1].split(']')[0]
            url_start = line.find('(')
            url_end = line.find(')')
            ref_url = line[url_start+1:url_end]
            ref_text_name = line[:url_start].split(']')[-1].strip()
            clickable_text = f'<a href="{ref_url}">{ref_text_name}</a>'
            formatted_references.append(f'[{ref_number}] {clickable_text}')
    
    formatted_references_text = 'References: ' + ', '.join(formatted_references)
    return main_text + '\n\n' + formatted_references_text

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
        
        # Format the response and references section
        for choice in response.choices:
            formatted_content = format_references(choice.message.content)
            choice.message.content = format_response(formatted_content)  # Removed remove_after_references
        
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