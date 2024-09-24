prompt = '''
Describe in a paragraph what is happening in this screenshot of a realistic person with a fruit/vegetable as their face. Try not to include too many small, intricate details about the image. Don't include or mention the actual fruit/vegetable in the prompt. The image will contain a realistic person with a fruit/vegetable as their face, so keep the caption to something like this: 'a person with a (expression type) expression in a <simple description of the background>. Keep it short.

Do NOT describe/include any of these intrinsic aspects about the image -

hyper-realistic, realistic, photograph, textures, lighting, professionalism, illustrated, screenshot, image, create, texture'''

from pydantic import BaseModel
from openai import OpenAI
import os

class CalendarEvent(BaseModel):
    output: str

import base64

# OpenAI API Key
api_key = "YOUR OPEN AI API KEY"
client = OpenAI(api_key=api_key)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def main(i):
    image_path = f"lora_set_v3/{i}.jpg"
    base64_image = encode_image(image_path)
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt,
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ],
        }
    ],
    response_format=CalendarEvent,
    )

    event = completion.choices[0].message.parsed
    final_prompt = event.output

    folder_path = "final_lora_captions_v2"

    txt_file_name = f"{i}.txt"
    txt_file_path = os.path.join(folder_path, txt_file_name)
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(final_prompt)
    print("done ", i)

if __name__ == "__main__":
    for i in range(0, 100):
        main(i)
