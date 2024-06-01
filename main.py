from PIL import Image
import requests
from io import BytesIO
from termcolor import colored
import urllib
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

def load_clipdrop_api_token() -> str:
    global clipdrop_api_token
    clipdrop_api_token = open("clipdrop.token", "r").read()


def get_screen_resolution():
    if os.name == "nt":
        width = ctypes.windll.user32.GetSystemMetrics(0)
        height = ctypes.windll.user32.GetSystemMetrics(1)
    else:
        width, height = 1920, 1080
    
    return width, height

def get_image(source, query) -> Image:
    width, height = get_screen_resolution()
    
    Stable_Diffusion_URLS = {
        "1.4": "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
        "1.5": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
        "2": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        "2.1": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
        "oj-v4": "https://api-inference.huggingface.co/models/prompthero/openjourney-v4"
    } # SDversion: URL
    
    def __image_from_url(url) -> Image:
        urllib.request.urlretrieve(url, "temp.jpg")
        img = Image.open("temp.jpg")
        return img
    
    def _get_image_from_Stable_Diffusion(version) -> Image:
        headers = {"Authorization": "Bearer " + hugging_face_api_token}
        parameters = {"use_cache": False, "wait_for_model": True}
        
        payload = {"inputs": "a picture of " + query}
        url = Stable_Diffusion_URLS[version]
        return Image.open(BytesIO(requests.post(url, headers=headers, json=payload, params=parameters).json()[0]["generated_text"].replace("a picture of ", "")))
    
    def _Clipdrop_Stable_Diffusion() -> Image:
        load_clipdrop_api_token()
        url = "https://clipdrop-api.co/text-to-image/v1"
        
        r = requests.post(url,
                            files = {"prompt": (None, "a picture of " + query)},
                          
                            headers = { "x-api-key": clipdrop_api_token }
                          )
        
        if r.ok:
            return Image.open(BytesIO(r.content))
        else:
            print("Error: " + r.text)
            return None
    
    def _wikimedia_commons():
        tag = "Q729" #Animal
        
        wikidata_api_endpoint = "https://commons.wikimedia.org/w/api.php"
        wikidata_params = {
            "action": "wbgetclaims",
            "format": "json",
            "entity": tag,
            "property": "P373" #wikimedia commons category
        }
        
        r = requests.get(wikidata_api_endpoint, params=wikidata_params)
        if r.ok:
            category = r.json()["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"]
        else:
            print("Error: " + r.text)
            return None
        
        wikimedia_api_endpoint = "https://commons.wikimedia.org/w/api.php"
        commons_params = {
            "action": "query",
            "format": "json",
            "list": "random",
            "cmtitle": "Category:" + category,
            "rnnamespace": "6",
            "rnlimit": "1"
        }
        
        r = requests.get(wikimedia_api_endpoint, params=commons_params)
        data = r.json()
        
        image_title = data["query"]["random"][0]["title"]
        
        image_info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={image_title}&prop=imageinfo&iiprop=url&format=json"

        r = requests.get(image_info_url)
        data = r.json()
        image_url = data["query"]["pages"][list(data["query"]["pages"].keys())[0]]["imageinfo"][0]["url"]
        
        img = __image_from_url(image_url)
        return img
        
        
    def _get_image_from_google_maps(query):
        pass
    
    
    img = None
    try:    
        match source:
            case "unsplash": img = Image.open(BytesIO(requests.get(f"https://source.unsplash.com/{width}x{height}/?{query}").content))
            case "SD-1.4": img = _get_image_from_Stable_Diffusion("1.4")
            case "SD-1.5": img = _get_image_from_Stable_Diffusion("1.5")
            case "SD-2": img = _get_image_from_Stable_Diffusion("2")
            case "SD-2.1": img = _get_image_from_Stable_Diffusion("2.1")
            case "oj-v4": img = _get_image_from_Stable_Diffusion("oj-v4")
            case "SDXL1": img = _Clipdrop_Stable_Diffusion()
            case "wikimedia": img = _wikimedia_commons()
            case _: print("Error: Unknown image source")
    except Exception as e:
        print(e)
        err = True
    else:
        err = False
    
    
    return img, err
    

def choose_image_subject(source, verbose=False) -> (str, bool):
    global image_topics
    
    subject = random.choice(image_topics)
    
    if verbose:
        print(f"Subject: {subject}")
    
    prompts = {
        "Open-Assistant": f"<|prompter|>Answer only using only Artistic Tokens such as `highly detailed` or `landscape`. Write only using tokenized words, not sentences, the artistic devices used in a picture of a {subject}<|endoftext|>",
        "GPT-3.5": f"Give me a detailed description of an image of a {subject}. Write only using tokenized words, not sentences."
    } # {AI-Model: Prompt}
    
    try:
        match source:
            case "simple": subject = f"A picture of {subject}"
            case "Open-Assistant": headers = {"Authorization": "Bearer " + hugging_face_api_token}; parameters = {"max_new_tokens": -1, "return_full_text": False}; subject =  f"A picture of {subject}, " + requests.post("https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5", headers=headers, json={"inputs": prompts["Open-Assistant"]}, params=parameters).json()[0]["generated_text"].replace(prompts["Open-Assistant"], "")
            case "gpt-2-sdpg": headers = {"Authorization": "Bearer " + hugging_face_api_token}; parameters = {"return_full_text": True}; subject =  f"A picture of {subject}, " + requests.post("https://api-inference.huggingface.co/models/Ar4ikov/gpt2-650k-stable-diffusion-prompt-generator", headers=headers, json={"inputs": subject}, params=parameters).json()[0]
    except:
        subject = f"A picture of {subject}"
        err = True
    else:
        err = False
        
    return subject, err

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
    abs_img_path = os.path.abspath(image_path)
    if os.name == "nt":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_img_path, 0)
        return False
    else:
        print("Not supported on this OS")
        return True


def main():
    #load_openAI_api_token()
    load_image_topics()
    
    prompt_sources = ["simple", "Open-Assistant", "gpt-2-sdpg"]
    image_sources = ["unsplash", "SD-1.4", "SD-1.5", "SD-2", "SD-2.1", "oj-v4", "SDXL1", "wikimedia"]
    
    promt_source = prompt_sources[0]
    image_source = image_sources[7]
    
    p = "calling " + promt_source + "... (1/3)"
    print(colored(p, "yellow"))
    
    prompt, err = choose_image_subject(promt_source, verbose=False)
    
    p = "calling " + promt_source + "... done"
    if err:
        print(colored(p, "red"))
    else:
        print(colored(p, "green"))
    
    

    p = "calling " + image_source + "... (2/3)"
    print(colored(p, "yellow"))
    
    img, err = get_image(image_source, prompt)
    
    if err:
        p = "calling " + image_source + "... failed"
        print(colored(p, "red"))
        return
    else:
        p = "calling " + image_source + "... done"
        print(colored(p, "green"))
    
    p = "setting wallpaper... (3/3)"
    print(colored(p, "yellow"))
    
    img.save("background.bmp")
    
    err = set_wallpaper("background.bmp")
    
    if err:
        p = "setting wallpaper... failed"
        print(colored(p, "red"))
        return
    else:
        p = "setting wallpaper... done"
        print(colored(p, "green"))
    
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