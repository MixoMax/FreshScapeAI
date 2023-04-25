from PIL import Image
import requests
from io import BytesIO
import os
import ctypes
import random
import time
import datetime

global hugging_face_api_token, openAI_api_token
global image_topics

hugging_face_api_token = "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"


def load_image_topics():
    global image_topics
    image_topics = []
    with open("image_topics.txt", "r") as f:
        for line in f.readlines():
            image_topics.append(line.strip())

def load_openAI_api_token():
    global openAI_api_token
    openAI_api_token = open("openai.token", "r").read()



def get_screen_resolution():
    if os.name == "nt":
        width = ctypes.windll.user32.GetSystemMetrics(0)
        height = ctypes.windll.user32.GetSystemMetrics(1)
    else:
        width, height = 1920, 1080
    
    return width, height

def get_image(source, query):
    width, height = get_screen_resolution()
    
    Stable_Diffusion_URLS = {
        "1.4": "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
        "1.5": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
        "2": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        "2.1": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
        "oj-v4": "https://api-inference.huggingface.co/models/prompthero/openjourney-v4"
    } # SDversion: URL
    
    def _get_image_from_Stable_Diffusion(version):
        headers = {"Authorization": "Bearer " + hugging_face_api_token}; parameters = {"use_cache": False, "wait_for_model": True}; return Image.open(BytesIO(requests.post(Stable_Diffusion_URLS[version], headers=headers, json={"inputs": "a picture of " + query}).content))
    
    match source:
        case "unsplash": return Image.open(BytesIO(requests.get(f"https://source.unsplash.com/{width}x{height}/?{query}").content))
        case "SD-1.4": return _get_image_from_Stable_Diffusion("1.4")
        case "SD-1.5": return _get_image_from_Stable_Diffusion("1.5")
        case "SD-2": return _get_image_from_Stable_Diffusion("2")
        case "SD-2.1": return _get_image_from_Stable_Diffusion("2.1")
        case "oj-v4": return _get_image_from_Stable_Diffusion("oj-v4")
    
    def get_image_from_google_maps(query):
        pass

def choose_image_subject(source, verbose=False):
    global image_topics
    
    subject = random.choice(image_topics)
    
    if verbose:
        print(f"Subject: {subject}")
    
    prompts = {
        "Open-Assistant": f"<|prompter|>Answer only using only Artistic Tokens such as `highly detailed` or `landscape`. Write only using tokenized words, not sentences, the artistic devices used in a picture of a {subject}<|endoftext|>",
        "GPT-3.5": f"Give me a detailed description of an image of a {subject}. Write only using tokenized words, not sentences."
    } # {AI-Model: Prompt}
    
    match source:
        case "simple": return subject
        case "Open-Assistant": headers = {"Authorization": "Bearer " + hugging_face_api_token}; parameters = {"max_new_tokens": -1, "return_full_text": False}; return f"A picture of {subject}, " + requests.post("https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5", headers=headers, json={"inputs": prompts["Open-Assistant"]}, params=parameters).json()[0]["generated_text"].replace(prompts["Open-Assistant"], "")
        case "gpt-2-sdpg": headers = {"Authorization": "Bearer " + hugging_face_api_token}; parameters = {"return_full_text": True}; return f"A picture of {subject}, " + requests.post("https://api-inference.huggingface.co/models/Ar4ikov/gpt2-650k-stable-diffusion-prompt-generator", headers=headers, json={"inputs": subject}, params=parameters).json()[0]


def add_image_subject(subject):
    global image_topics
    image_topics.append(subject)
    with open("image_topics.txt", "a") as f:
        f.write(subject)

def remove_image_subject(subject):
    global image_topics
    image_topics.remove(subject)
    with open("image_topics.txt", "w") as f:
        for topic in image_topics:
            if topic != "" and topic != subject:
                f.write(topic)



def set_wallpaper(image_path):
    abs_img_path = os.path.abspath("background.bmp")
    if os.name == "nt":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_img_path, 0)
    else:
        print("Not supported on this OS")


def main():
    #load_openAI_api_token()
    load_image_topics()
    
    prompt_sources = ["simple", "Open-Assistant", "gpt-2-sdpg"]
    image_sources = ["unsplash", "SD-1.4", "SD-1.5", "SD-2", "SD-2.1", "oj-v4"]
    
    promt_source = prompt_sources[1]
    image_source = image_sources[5]
    
    print("calling " + promt_source + "...")
    
    prompt = choose_image_subject(promt_source, verbose=False)
    
    

    print("calling " + image_source + "...")
    
    img = get_image(image_source, prompt)
    
    img.save("background.bmp")
    
    img.show()
    
    print("image prompt: " + prompt)
    
    #save_to_fav = input("Save to favorites? (y/n): ")
    save_to_fav = "n"
    
    if save_to_fav == "y":
        if os.path.exists("./favorites") == False:
            os.mkdir("./favorites")
        i = 0
        while True:
            img_name = prompt.replace(" ", "_").replace(",", "") + "_" + str(i) + ".bmp"
            if os.path.exists("./favorites/" + img_name):
                i += 1
            else:
                img.save("./favorites/" + img_name)
                print("saved to favorites as " + img_name)
                break


if __name__ == "__main__":
    main()