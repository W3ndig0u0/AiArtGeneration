import torch
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
        artModel_id,
        initial_generation=False,
    ):
        if initial_generation:
            self.progress = 0
        self.total_steps = batch_size
        self.generation_complete = False
        self.estimated_time = None

        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
        elif torch.cuda.is_available():
            torch.cuda.empty_cache()

        model_folder = "./artModel"
        # model_id = "Ojimi/anime-kawai-diffusion"
        print(artModel_id)
        # model_id = "andite/pastel-mix"
        self.generator = load_modelDiff(artModel_id, model_folder, self.device)
        print(self.device)
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

            os.makedirs(save_folder, exist_ok=True)

            existing_files = os.listdir(save_folder)
            file_count = len(existing_files)
            randomSeed = [
                torch.Generator(self.device).manual_seed(seed)
                if batch_size == 1
                else torch.Generator(self.device).manual_seed(seed + step)
                for step in range(batch_size)
            ]
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
            elif torch.cuda.is_available():
                torch.cuda.empty_cache()

            start_time = time.time()
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
                    save_path = os.path.join(save_folder, f"{file_number}.png")
                    image.save(save_path)

                self.progress = step + 1

                elapsed_time = time.time() - start_time
                if step > 0:
                    average_time_per_step = elapsed_time / step
                    remaining_steps = num_inference_steps - step
                    estimated_time = average_time_per_step * remaining_steps
                    self.estimated_time = round(estimated_time, 2)

            final_file_number = file_count + num_inference_steps * batch_size

            self.generation_complete = True
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
            elif torch.cuda.is_available():
                torch.cuda.empty_cache()

        return save_folder, file_number


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
        "bad art",
        save_folder,
        seed,
        batch_size,
        initial_generation,
    )
