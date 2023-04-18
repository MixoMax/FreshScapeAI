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
        
        chosen_subject = random.choice(potential_image_subjects)
        
        input_str = f"Imagine you are a photographer in a specific environment, and you see a beautiful sculpture of {chosen_subject} in that environment. Choose an appropriate environment for {chosen_subject} (for example, if the subject is (frog) the environment could be a jungle) and describe a picture of {chosen_subject} using adjectives that describe Photographic and Artistic qualities, answering the question (What is the mood or feeling you want to convey in this image?)."
        
        response = requests.post(API_URL, headers=headers, json={
            "inputs": input_str,
            "parameters": {
                "max_new_tokens": 250,
                "temperature": 0.9,
                "top_p": 0.95,
                "top_k": 50,
                "repetition_penalty": 20,
                "return_full_text": False
            },
            "options": {"use_cache": False, "wait_for_model": True}
            })
        
        response_text = response.json()[0]["generated_text"]
        
        print(chosen_subject)
        
        print(response.status_code)
        
        if response_text == "":
            return choose_image_subject(ai_enabled=True)
        
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

