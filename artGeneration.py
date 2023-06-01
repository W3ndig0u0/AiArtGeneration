import os
import torch
from diffusers import DiffusionPipeline
from PIL import Image
from accelerate import Accelerator

class AnimeArtist:
    def __init__(self):
        self.model_id = "stablediffusionapi/anime-model-v2"
        self.cache_dir = "./animeModel"
        self.device = self.get_device()
        self.generator = self.load_art_model()

    def get_device(self):
        if torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")

    def load_art_model(self):
        model_name = self.model_id
        cache_dir = self.cache_dir
        device = self.device

        os.makedirs(cache_dir, exist_ok=True)

        model_dir = os.path.join(cache_dir, model_name.replace('/', '-'))

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            pipeline = DiffusionPipeline.from_pretrained(model_name)
            pipeline.save_pretrained(model_dir)
        else:
            pipeline = DiffusionPipeline.from_pretrained(model_dir)

        pipeline.sampling_method = "dpm++-2M-karras"
        pipeline.depth = 20
        pipeline.gradient_checkpointing = True

        accelerator = Accelerator()
        generator = accelerator.prepare(pipeline)

        return generator

    def generate_art(self, prompt, num_inference_steps, eta, guidance_scale):
        with torch.no_grad():
            generator = self.generator
            current_image = None

            for step in range(num_inference_steps):
                prompt_with_image = f"{prompt} {current_image}" if current_image else prompt

                generated = generator(prompt_with_image, eta=eta, guidance_scale=guidance_scale)
                current_image = generated.images[0]
                print(prompt_with_image);
                current_image.save(f"anime-art-{step}.png")

if __name__ == '__main__':
    anime_artist = AnimeArtist()
    prompt = "Masterpiece, cute girl, fantasy, jump pose"
    num_inference_steps = 1
    eta = 0.1
    guidance_scale = 1
    anime_artist.generate_art(prompt, num_inference_steps, eta, guidance_scale)
