import os
import torch
from diffusers import DiffusionPipeline
from PIL import Image
from accelerate import Accelerator
from loadModel import load_model

class AnimeArtist:
    def __init__(self):
        self.model_id = "stablediffusionapi/anime-model-v2"
        self.cache_dir = "./animeModel"
        self.device = self.get_device()
        self.generator = self.load_model()

    def get_device(self):
        if torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")

def load_model(self):
    model_name = self.model_id
    cache_dir = self.cache_dir
    device = self.device

    prompt_input = request.form.get('prompt-input')
    num_inference_steps = int(request.form.get('num-inference-steps-slider'))
    eta = float(request.form.get('eta-slider'))
    guidance_scale = int(request.form.get('guidance-scale-slider'))
    negative_prompt = request.form.get('negative-prompt-input')

    model, tokenizer = load_model(model_name, cache_dir, device)
    generator = DiffusionPipeline.from_pretrained_model(model)
    generator.set_tokenizer(tokenizer)
    generator.negative_prompt = negative_prompt
    generator.sampling_method = "dpm++-2M-karras"
    generator.depth = num_inference_steps
    generator.enable_attention_slicing()
    generator.gradient_checkpointing = True  # Enable gradient checkpointing

    generator = accelerator.prepare(generator)
    return generator


    def generate_art(self, prompt, num_inference_steps, eta, guidance_scale):
        with torch.no_grad():
            generator = self.generator
            generator.generator.eval()  # Set generator to evaluation mode
            current_image = None

            for step in range(num_inference_steps):
                # Perform a single inference step
                current_image = generator(prompt, current_image=current_image, eta=eta, guidance_scale=guidance_scale).images[0]
                current_image.save(f"anime-art-{step}.png")

if __name__ == '__main__':
    accelerator = Accelerator()
    anime_artist = AnimeArtist()
    anime_artist.generate_art()
