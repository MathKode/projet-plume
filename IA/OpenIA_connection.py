from openai import OpenAI

def IA_upload_openIA(apikey, file_path):
    client = OpenAI(
        api_key=apikey
    )
    r = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants",
        expires_after={
            "anchor": "created_at",
            "seconds": 3600
        }
    )
    #print(r)
    return r.id

def IA_ask_openIA(apikey,prompt,file_id_ls,nom_model):
    openai_models = [
        # GPT‑5
        "gpt-5.4",
        "gpt-5.4-pro",
        "gpt-5.2",
        "gpt-5.2-pro",
        "gpt-5.1",
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano",

        # GPT‑4.1
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4.1-nano",

        # Modèles images
        "gpt-image-1",
        "gpt-image-1.5",
        "gpt-image-1-mini",

        # Open‑source / alternatifs
        "gpt-oss-120b",
        "gpt-oss-20b"
    ]

    client = OpenAI(
        api_key=apikey
    )

    content_list = [{"type": "input_text", "text": f"{prompt}"}]
    for file_id in file_id_ls:
        content_list.append(
               {"type": "input_file", "file_id": file_id},
        )

    response = client.responses.create(
        model=nom_model,
        input=[{
            "role": "user",
            "content": content_list
        }]
    )

    client.close()
    #print(response.output_text)
    return response.output_text
