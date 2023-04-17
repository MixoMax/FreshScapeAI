from PIL import Image
import requests
from io import BytesIO
import os
import ctypes
import random
import sys


def get_unsplash_image(query, width, height):
    print(query)
    url = f"https://source.unsplash.com/{width}x{height}/?{query}"
    response = requests.get(url)
    print(response.status_code)
    return Image.open(BytesIO(response.content))

def get_stable_diffusion_image_huggingface(query, width, height):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    
    hugging_face_api_token = "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"
    
    headers = {"Authorization": "Bearer " + hugging_face_api_token}
    
    response = requests.post(API_URL, headers=headers, json={"inputs": "a picture of " + query})
    
    print(response.status_code)
    
    print(query)
    
    return Image.open(BytesIO(response.content))



def set_background_image(query, width, height, ai_enabled = False):
    image = get_unsplash_image(query, width, height) if ai_enabled == False else get_stable_diffusion_image_huggingface(query, width, height)
    image.save("background.bmp")
    operating_system = os.name
    
    if operating_system == "nt":
        abs_img_path = os.path.abspath("background.bmp")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_img_path, 0)
    elif operating_system == "posix":
        print("Linux support coming soon!")
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{os.getcwd()}/background.bmp")

def choose_image_subject(ai_enabled = False):
    
    potential_image_subjects = [  "Flower",  "Mountain",  "Sunset",  "Ocean",  "Forest",  "River",  "Sky",  "Beach",  "Waterfall",  "Butterfly",  "Star",  "Snowflake",  "Bird",  "Tree",  "Wave",  "Cloud",  "Sunflower",  "Rock",  "Rainbow",  "Butterfly", "Candle",  "Coffee",  "Book",  "Castle",  "Rain",  "Moon",  "Bridge",  "Lighthouse",  "Sailboat",  "Train",  "Bicycle",  "Car",  "Mountain Range",  "Squirrel",  "Eagle",  "Frog",  "Ladybug",  "Dragonfly",  "Honeybee",  "Mushroom", "Skyscraper",  "Cathedral",  "Basilica",  "Pagoda",  "Temple",  "Taj Mahal",  "Colosseum",  "Parthenon",  "Chateau",  "Fortress" ]
    
    if ai_enabled == False:

        chosen_subject = random.choice(potential_image_subjects)
        
        return chosen_subject
    
    else:
        # do an api call to an ai to sugest an image subject
        hugging_face_api_token = "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"
        
        API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-1-pythia-12b"
        
        headers = {"Authorization": "Bearer " + hugging_face_api_token}
        
        input_str = f"""transform any given input to Stable Diffusion Prompt:

|Original|Stable Diffusion Prompt|
|:---|:---|
|Keanu Reeves as an asian warrior chief|Keanu Reeves portrait photo of a asia old warrior chief, tribal panther make up, blue on red, side profile, looking away, serious eyes, 50mm portrait photography, hard rim lighting photography–beta –ar 2:3 –beta –upbeta –beta –upbeta –beta –upbeta|
|a priest in a blue robe|priest, blue robes, 68 year old man, national geographic, portrait, photo, photography –s 625 –q 2 –iw 3|
|girl with headphones|gorgeous young Swiss girl sitting by window with headphones on, wearing white bra with translucent shirt over, soft lips, beach blonde hair, octane render, unreal engine, photograph, realistic skin texture, photorealistic, hyper realism, highly detailed, 85mm portrait photography, award winning, hard rim lighting photography–beta –ar 9:16 –s 5000 –testp –upbeta –upbeta –upbeta|
|Ruined temple|temple in ruines, forest, stairs, columns, cinematic, detailed, atmospheric, epic, concept art, Matte painting, background, mist, photo-realistic, concept art, volumetric light, cinematic epic + rule of thirds octane render, 8k, corona render, movie concept art, octane render, cinematic, trending on artstation, movie concept art, cinematic composition , ultra-detailed, realistic , hyper-realistic , volumetric lighting, 8k –ar 2:3 –test –uplight|
|Panorama of a futuristic city |  A grand city in the year 2100, atmospheric, hyper realistic, 8k, epic composition, cinematic, octane render, artstation landscape vista photography by Carr Clifton & Galen Rowell, 16K resolution, Landscape veduta photo by Dustin Lefevre & tdraw, 8k resolution, detailed landscape painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, Breath of The Wild, 4k detailed post processing, artstation, rendering by octane, unreal engine —ar 16:9 |
|Painting of the San Francisco Bridge |  an expressive gouache painting of San Francisco bay bridge, sunset, photorealistic |
|Woman with ginger Hair| ultra detailed, detailed, girl with medium lenght ginger hair, cinematic, white t-shirts |
|Stylized Funko Pop in a field | funko style of hyperrealistic full length portrait of gorgeous goddess, standing in field full of flowers, intricate, elegant, realistic, cinematic, character design, concept art, highly detailed, illustration, digital art, digital painting, depth of field |

transform the inputs i give into a detailed, specific, and vivid description that includes various visual and technical details. DO NOT WRITE A TEXT, WRITE A DESCRIPTION, seperate each description with a comma.


Generate a description of {random.choice(potential_image_subjects)} using Stable Diffusion Prompt:


A Picture of..."""
        
        response = requests.post(API_URL, headers=headers, json={
            "inputs": input_str,
            "parameters": {
                "max_new_tokens": 250,
                #"temperature": 0.9,
                #"top_p": 0.95,
                #"top_k": 50,
                "repetition_penalty": 20,
                "return_full_text": False
            },
            "options": {"use_cache": False, "wait_for_model": True}
            })
        
        response_text = response.json()[0]["generated_text"]
        
        print(response.status_code)
        
        return response_text
        

def get_screen_resolution():

    user32 = ctypes.windll.user32

    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
    return screen_width, screen_height


if __name__ == "__main__":

    ai_enabled = False

    subject = choose_image_subject(ai_enabled)
    
    print(f"Subject: {subject}")
    
    

    set_background_image(subject, *get_screen_resolution(), ai_enabled)

