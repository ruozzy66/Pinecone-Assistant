import sys
import json
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def format_references(text):
    """Format the references section with improved styling and clickable links."""
    if 'References:' not in text:
        return text
    
    parts = text.split('References:')
    main_text = parts[0].strip()
    references_text = parts[1].strip()
    
    # Dictionary to store file names and their corresponding URLs
    file_links = {
        'TI4_CompleteRulesReference_Feb_07_2022.pdf': 'https://storage.googleapis.com/knowledge-prod-files/1d469cc4-da32-4872-b2c1-615d01fbc939%2F24a4dd03-45ad-4041-8677-1d7b4e5da31a%2Fa2193e55-b6f5-418d-aa1b-e290384d7a65.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=ke-prod-1%40pc-knowledge-prod.iam.gserviceaccount.com%2F20240803%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240803T043521Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&response-content-disposition=inline&response-content-type=application%2Fpdf&X-Goog-Signature=abacbd7f858413b507b526aeb9e2fdb74a6a7ac45e2e92c4985231b552d21121108ff0c7c5c1eae3ef68646a3f7ce1e1e2424affaa76f51cd600dab34ba73b93a38dcbf9632888243f28170263a16af0541f2ab036234bc17b223eeba4035204734d1f6dd2ffcc953a121b392b696958b0c17abf1a030b58b8853f9cb0dc2e1f45dee08251581922ed93696db3420b09cc71736b888ee180d3ffd82f7ad9e754dfe2a43b1cd04438b0fb6e1762bca162fc4860b3e0adcb57502ff41eeed4a8bd62a010762bbbabbb9ed0d6a3a9dc5c07d88fc752a965aa87cd1822e79f93e9db5ef5821f5032e4cc5fb8d192b90b58f32c6992da13cc368b39864d24e85ac8b6',
        'Game_Play_Reference_v1.pdf': 'https://storage.googleapis.com/knowledge-prod-files/1d469cc4-da32-4872-b2c1-615d01fbc939%2F24a4dd03-45ad-4041-8677-1d7b4e5da31a%2F37916079-a873-4a85-aef2-aa7ece1a2264.pdf?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=ke-prod-1%40pc-knowledge-prod.iam.gserviceaccount.com%2F20240803%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240803T043521Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&response-content-disposition=inline&response-content-type=application%2Fpdf&X-Goog-Signature=3748f3039ce390ed3f1f32e3be15fb7cc14356816e9af0348060f378f60a7a355db1643529fec2393538640487febc1afd213fb18c25a76d278c433b56acc6514e1548a4ef61203842e3d50d63a3ece7633c6ce447c139ad212feea856fa1aafaea00a80c5cdda1b588bb2007eab18ec14afa0b0c27be411fb7b710f3ce90b97def0117672db7e943684430274136798ceb05303f8912217cc34b2a138fb1c420157e44c917e0ddc900bc54fc1a7f20e6487895b66f3d5784cc70eeb0bde98a1c9090873c968cbe77028ce662a27c0e313d58c6e299b258bcf963ca394c03c5b86aa47da557c006b43da70fab94f9672603bb822a98a690891671f1e4bbd6337'
    }
    
    formatted_references = []
    for line in references_text.split('\n'):
        line = line.strip()
        if line:
            if line.startswith('[') and ']' in line:
                # This is a file reference
                ref_number = line.split('[')[1].split(']')[0]
                file_name = line.split(']')[1].strip()
                if file_name in file_links:
                    formatted_line = f'[{ref_number}] <a href="{file_links[file_name]}">{file_name}</a>'
                else:
                    formatted_line = line
            else:
                # This is a regular reference
                formatted_line = line
            formatted_references.append(formatted_line)
    
    formatted_references_text = '<br><br><b>References:</b><br>' + '<br>'.join(formatted_references)
    return main_text + formatted_references_text

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