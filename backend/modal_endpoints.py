import modal
import fal_client
from pydantic import BaseModel
import random

stub = modal.Stub("luma")

fal_key = "YOUR FAL API KEY"
openai_api_key = "YOUR OPEN AI API KEY"
import os
os.environ['FAL_KEY'] = fal_key

from openai import OpenAI
client = OpenAI(api_key=openai_api_key)
image = (
    modal.Image.debian_slim()
    .pip_install(
        "fal-client", 
        "openai"
    )
)

class CalendarEvent(BaseModel):
    output: str

prompt_template = f"""Create a hyper-realistic photograph of a person with a random fruit/vegetable for a head. The random fruit/vegetable has "lifelike human eyes", and a realistic expression. The random fruit/vegetable should have a realistic facial expression with a realistic mouth and face."""

def get_gpt4_response(prompt):
    
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a creative AI assistant specializing in generating unique and detailed prompts for hyper-realistic surreal photographs."},
                {"role": "user", "content": f"Improve this existing prompt for a realistic photograph of a person with a fruit/vegetable for a head, based on this template. \n\n{prompt_template}. Here is the actual user created prompt that you need to improve. Do not make the improved prompt too long. {prompt}"}
            ],
            response_format=CalendarEvent,
        )
        event = completion.choices[0].message.parsed
        return event.output
    except Exception as e:
        return f"An error occurred: {str(e)}"

@stub.function(image=image)
@modal.web_endpoint(method="POST", label="all-luma-endpoints")
def serve_code(item: dict):
    prompt = item.get("prompt")
    version = item.get("version")

    if version == "v1":
        handler = fal_client.submit(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "image_size": "square_hd", 
                "enable_safety_checker": False
            },
        )
        result = handler.get()
        url = result['images'][0]['url']
        print("URL", url)
        return {"url": url}
    elif version == "v2":
        improved_prompt = get_gpt4_response(prompt)
        print("improved prompt", improved_prompt)
        handler = fal_client.submit(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": improved_prompt,
                "image_size": "square_hd", 
                "enable_safety_checker": False
            },
        )
        result = handler.get()
        print(result)
        result = handler.get()
        url = result['images'][0]['url']
        return {"url": url, "prompt": improved_prompt}
    elif version == "v3":
        lora_strength = item.get("strength", 1.0)
        handler = fal_client.submit(
            "fal-ai/flux-lora",
            arguments={
                "prompt": prompt,
                "model_name": None,
                "loras": [{
                    "path": "https://storage.googleapis.com/fal-flux-lora/8123f6b8c93f4f06828f830113749fff_lora.safetensors",
                    "scale": lora_strength  #1
                }],
                "embeddings": [], 
                "image_size": "square_hd", 
                "enable_safety_checker": False
            },
        )

        result = handler.get()
        print(result)
        result = handler.get()
        url = result['images'][0]['url']
        return {"url": url}