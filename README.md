# FreshScapeAI 

Python script to Auto-Prompt a reverse Diffusion Model using a LLM to generate a new Background Image on startup.

## Disclaimer

Most recent Prototype is just a Proof of Concept and will only work in Windows.

Currently, the script only works with Unsplash Images, as the Stable Diffusion Model is not yet properly integrated as i couldn't find a free API that can be used to generate images above 512x512px. It will technicall work, but the images will be very low quality.

## Requirements

- Python 3.6
- requests (pip install requests)
- Pillow (pip install Pillow)
- Internet Connection

## Usage

to generate a new Background Image, run:

    python Wallpaper-Changer.py

to automatically run the script on startup, run:

    register.py

## Supported Models

LLMs:

- [Open Assistant](https://www.open-assistant.io/), a free and open source AI assistant by LAION
- [gpt2-650k-stable-diffusion-prompt-generator](https://huggingface.co/Ar4ikov/gpt2-650k-stable-diffusion-prompt-generator) a gpt 2 based model, fine tuned for stable diffusion prompts
- More to come

Image Generators:

- [Stable Diffusion](https://stability.ai/stable-diffusion/), a free and open source image generator by StabilityAI:
    - 1.4
    - 1.5
    - 2
    - 2.1
- [unsplash](https://unsplash.com) While not a model, it is a great source for free images, which also can be used as a background image and most of the time, they are pretty good.

Considered Models for future releases:

LLMs:
- GPT-3.5 Turbo / 4
- LLama Based LLMs

Image Generators:
- Dalle (1/2)
- Gan based Image Generators
- More Stable Diffusion Versions and sub-models (such as Midjourney, protogen)

## How it works

The script 

## Credits

I would like to thank the following people for their work:
- LAION for their huge work towards Open source AI
- Yannic Kilcher for his incrdible work on the Open Assistant LLM
- RunwayML and StabilityAI for one of the greatest, open source models, that is Stable Diffusion

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

However, the models used in this project may be licensed differently. Please check the respective license of the models you use.