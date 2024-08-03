import sys
import json
import re
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def format_references(text):
    """Format the references section with improved styling and clickable links."""
    if 'References:' not in text:
        return text
    
    parts = text.split('References:')
    main_text = parts[0].strip()
    references_text = parts[1].strip()
    
    # Use regex to match the entire reference line
    pattern = r'(\d+)\.\s+(\S+)'  # Adjusted regex to match the file name pattern
    formatted_references = []
    for match in re.finditer(pattern, references_text):
        ref_number, file_name = match.groups()
        formatted_line = f'{ref_number}. <a href="{file_name}" target="_blank"><u>{file_name}</u></a>'
        formatted_references.append(formatted_line)
    
    formatted_references_text = '<p><b>References:</b></p>\n' + '<br>\n'.join(formatted_references)
    return main_text + '\n\n' + formatted_references_text

def format_response(text):
    """Format the response with bullet points and appropriate formatting."""
    lines = text.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Replace ** with <b> HTML tags for bold text
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        
        if line.startswith('* '):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            # Remove the asterisk and any leading number
            content = re.sub(r'^\*\s*(\d+\.\s*)?', '', line)
            formatted_lines.append(f'<li>{content}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            formatted_lines.append(f'<p>{line}</p>')
    
    if in_list:
        formatted_lines.append('</ul>')
    
    return '\n'.join(formatted_lines)

def chat_with_assistant(api_key, assistant_name, messages):
    try:
        pc = Pinecone(api_key=api_key)
        assistant = pc.assistant.describe_assistant(assistant_name)
        
        chat_context = [Message(**msg) for msg in json.loads(messages)]
        response = assistant.chat_completions(messages=chat_context)
        
        # Format the response and references section
        for choice in response.choices:
            formatted_content = format_references(choice.message.content)
            choice.message.content = format_response(formatted_content)
        
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
