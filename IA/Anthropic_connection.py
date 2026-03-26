from anthropic import Anthropic

def IA_upload_anthropic(apikey, file_name, file_path):
    client = Anthropic(
        # This is the default and can be omitted
        api_key=apikey,
    )
    r = client.beta.files.upload(
        file=(f"{file_name}", open(file_path, "rb"), "text/plain"),
    )
    client.close()
    return r.id

def IA_ask_anthropic(apikey,prompt,file_id_ls,nom_model):
    claude_models_api = [
        "claude-opus-4-6",
        "claude-opus-4-5",
        "claude-opus-4-1",
        "claude-opus-4",
        "claude-sonnet-4-6",
        "claude-sonnet-4",
        "claude-sonnet-3-7",
        "claude-haiku-4-5",
        "claude-haiku-3-5",
        "claude-haiku-3",
    ]
    client = Anthropic(
        # This is the default and can be omitted
        api_key=apikey,
    )
    content_list = [{"type": "text", "text": prompt}]
    for file_id in file_id_ls:
        content_list.append({
            "type": "document",
            "source": {
                "type": "file",
                "file_id": file_id
            }
        })

    message = client.beta.messages.create(
        max_tokens=10000,
        messages=[
            {
                "role": "user",
                "content": content_list
            }
        ],
        betas=["files-api-2025-04-14"],
        model=nom_model,
    )
    client.close()
    return "\n".join(message.content[0].text.split('\\n'))