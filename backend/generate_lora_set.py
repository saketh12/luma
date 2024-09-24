fal_key = "YOUR FAL API KEY"
openai_api_key = "YOUR OPEN AI API KEY"

import os
os.environ['FAL_KEY'] = fal_key
import fal_client
import openai
import random
from openai import OpenAI
from pydantic import BaseModel
import requests
import os
class CalendarEvent(BaseModel):
    output: str

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

def generate_prompt():
    expressions = ["neutral", "smiling", "serious", "thoughtful", "confident", "relaxed", "focused"]
    clothing = ["business suit", "casual outfit", "formal dress", "t-shirt and jeans", "sweater", "blouse", "button-up shirt"]
    backgrounds = ["office", "park", "beach", "city street", "home interior", "garden", "studio backdrop"]
    lighting = ["natural sunlight", "soft studio lighting", "dramatic side lighting", "warm golden hour glow", "cool blue tones"]

    prompt = f"""Create a hyper-realistic photograph of a person with a random fruit/vegetable for a head. The random fruit/vegetable has "lifelike human eyes", and a {random.choice(expressions)} expression. The random fruit/vegetable should have a realistic facial expression with a realistic mouth and face. The body is wearing a {random.choice(clothing)} and is positioned in a {random.choice(backgrounds)} setting. The lighting is {random.choice(lighting)}."""

    return prompt

def get_gpt4_response(prompt):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a creative AI assistant specializing in generating unique and detailed prompts for hyper-realistic surreal photographs."},
                {"role": "user", "content": f"Generate a prompt for a realistic photograph of a person with a fruit/vegetable for a head, based on this template. \n\n{prompt}"}
            ],
            response_format=CalendarEvent,
        )
        event = completion.choices[0].message.parsed
        return event.output
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main(i):


    folder_path = "lora_set_v3"
    img_file_path = os.path.join(folder_path, f"{i}.jpg")
    txt_file_path = os.path.join(folder_path, f"{i}.txt")

    if os.path.exists(img_file_path) and os.path.exists(txt_file_path):
        print(f"Skipping index {i} as both image and prompt already exist.")
        return

    base_prompt = generate_prompt()
    final_prompt = get_gpt4_response(base_prompt)
    handler = fal_client.submit(
    "fal-ai/flux/schnell",
    arguments={
        "prompt": final_prompt,
        "image_size": "square_hd", 
        "enable_safety_checker": False
        },
    )

    result = handler.get()
    url = result['images'][0]['url']
    folder_path = "lora_set_v3"
    response = requests.get(url)
    file_name = f"{i}.jpg" 
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print(f"File saved at: {file_path}")
    txt_file_name = f"{i}.txt"
    txt_file_path = os.path.join(folder_path, txt_file_name)
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(final_prompt)

if __name__ == "__main__":
    for i in range(0, 100):
        main(i)