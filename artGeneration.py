import os
from diffusers import DiffusionPipeline
from fileSize import print_available_models, get_folder_size, convert_size
from loadModel import load_model
from PIL import Image

def load_diffusion_pipeline(model_name, cache_dir):
    return DiffusionPipeline.from_pretrained(model_name, cache_dir=cache_dir)

class AnimeArtist:
    def __init__(self):
        self.cache_dir = './animeModel'
        self.load_model()
    
    def load_model(self):
        self.pipeline = load_diffusion_pipeline("stablediffusionapi/anime-model-v2", self.cache_dir)

    def generate_art(self):
        prompt = "1 cute girl, genshin impact"
        outputs = self.pipeline(prompt)
        image = outputs['image']
        image.save("generated_art.png")
        return image

if __name__ == '__main__':
    anime_artist = AnimeArtist()
    generated_image = anime_artist.generate_art()
    print("Generated art saved as generated_art.png")
