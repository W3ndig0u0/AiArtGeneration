import torch
from torch import mps

from PIL import Image
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
from loadModel import load_modelDiff
import time
import os
import random


class AnimeArtist:
    def __init__(self):
        self.progress = 0
        self.total_steps = 0
        self.generation_complete = False
        self.estimated_time = None
        self.generator = None
        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

    def generate_art(
        self,
        input_prompt,
        height,
        width,
        num_inference_steps,
        eta,
        negative_prompt,
        guidance_scale,
        save_folder,
        seed,
        batch_size,
        initial_generation=False,
    ):
        if initial_generation:
            self.progress = 0
        self.total_steps = num_inference_steps
        self.generation_complete = False
        self.estimated_time = None



        if torch.backends.mps.is_available():
            torch.mps.empty_cache()        
        elif torch.cuda.is_available():
            torch.cuda.empty_cache() 
            
        if self.generator is None:
            model_folder = "./artModel"
            # model_id = "Ojimi/anime-kawai-diffusion"
            model_id = "andite/pastel-mix"
            self.generator = load_modelDiff(model_id, model_folder, self.device)
            print(self.device)
            print(torch.cuda.is_available())
            print(torch.backends.mps.is_available())
            # self.generator.scheduler = EulerAncestralDiscreteScheduler(
            #     num_inference_steps
            # )
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()            
            elif torch.cuda.is_available():
                torch.cuda.empty_cache()           

        with torch.no_grad():
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()            
            elif torch.cuda.is_available():
                torch.cuda.empty_cache()     
            generator = self.generator.to(self.device)
            current_images = [
                Image.new("RGB", (width, height)) for _ in range(batch_size)
            ]
            intermediate_folder = os.path.join(str(save_folder), "intermediate")

            os.makedirs(intermediate_folder, exist_ok=True)

            existing_files = os.listdir(intermediate_folder)
            file_count = len(existing_files)
            randomSeed = [
                torch.Generator(self.device).manual_seed(seed)
                for _ in range(batch_size)
            ]

            if torch.backends.mps.is_available():
                torch.mps.empty_cache()            
            elif torch.cuda.is_available():
                torch.cuda.empty_cache()

            for step in range(batch_size):
                generated = generator(
                    prompt=input_prompt,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    eta=eta,
                    negative_prompt=negative_prompt,
                    generator=randomSeed,
                )



                if torch.backends.mps.is_available():
                    torch.mps.empty_cache()                
                elif torch.cuda.is_available():
                    torch.cuda.empty_cache()

                current_images = generated.images

                for i, image in enumerate(current_images):
                    file_number = file_count + step * batch_size + i + 1
                    save_path = os.path.join(intermediate_folder, f"{file_number}.png")
                    image.save(save_path)

                self.progress = step + 1

            final_file_number = file_count + num_inference_steps * batch_size

            self.generation_complete = True
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()           
            elif torch.cuda.is_available():
                torch.cuda.empty_cache()

        return intermediate_folder


if __name__ == "__main__":
    anime_artist = AnimeArtist()

    prompt = "Masterpiece, cute girl, fantasy, jump pose"
    num_inference_steps = 2
    eta = 0.1
    guidance_scale = 7
    save_folder = "./GeneratedImg"
    seed = [random.randint(0, 9999) for _ in range(num_inference_steps)]
    batch_size = 1

    anime_artist.generate_art(
        prompt,
        512,
        512,
        num_inference_steps,
        guidance_scale,
        eta,
        # "bad art",
        save_folder,
        seed,
        batch_size,
        initial_generation,
    )
