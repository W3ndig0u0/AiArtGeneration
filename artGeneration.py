import torch
from PIL import Image
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
from loadModel import load_modelDiff
import time
import os
import math
import random
import datetime


class AnimeArtist:
    def __init__(self):
        self.progress = 0
        self.total_steps = 0
        self.generation_complete = False
        self.estimated_time = None
        self.generator = None
        self.device = torch.device(
            "mps"
            if torch.backends.mps.is_available()
            else "cuda" if torch.cuda.is_available() else "cpu"
        )

    def load_generator(self, artModel_id, vae_name, model_folder):
        self.generator = load_modelDiff(
            artModel_id, vae_name, model_folder, self.device
        )
        self.generator.to(self.device)

    def image_grid(self, imgs, rows, cols, max_size):
        w, h = imgs[0].size
        max_size = min(max_size, 512)

        if w > max_size or h > max_size:
            aspect_ratio = w / h
            if aspect_ratio > 1:
                w = max_size
                h = int(w / aspect_ratio)
            else:
                h = max_size
                w = int(h * aspect_ratio)

        grid = Image.new("RGB", size=(cols * w, rows * h))
        for i, img in enumerate(imgs):
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            grid.paste(img, box=(i % cols * w, i // cols * h))
        return grid

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
        vae_name,
        initial_generation=False,
    ):
        model_folder = "./artModel"
        if initial_generation or self.generator is None:
            self.progress = 0

        self.load_generator(artModel_id, vae_name, model_folder)

        self.total_steps = batch_size
        self.generation_complete = False
        self.estimated_time = None

        print(vae_name)
        print(self.device)

        (
            torch.cuda.empty_cache()
            if torch.cuda.is_available()
            else torch.mps.empty_cache()
        )
        self.generator.enable_model_cpu_offload() if torch.cuda.is_available() else None
        self.generator.enable_attention_slicing()

        with torch.no_grad():
            current_images = [
                Image.new("RGB", (width, height)) for _ in range(batch_size)
            ]

            os.makedirs(save_folder, exist_ok=True)
            existing_files = [
                f
                for f in os.listdir(save_folder)
                if f.endswith(".png") and f.split(".")[0].isdigit()
            ]
            existing_numbers = [
                int(file_name.split("_")[-1].split(".")[0])
                for file_name in existing_files
            ]
            last_file_number = max(existing_numbers) if existing_numbers else 0

            date_prefix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            randomSeeds = [
                (
                    torch.Generator(self.device).manual_seed(seed)
                    if seed != -1 and step == 0
                    else torch.Generator(self.device).manual_seed(
                        torch.randint(0, 2**32, (1,)).item()
                    )
                )
                for step in range(batch_size)
            ]

            start_time = time.time()
            file_number = last_file_number

            for step in range(batch_size):
                generated = self.generator(
                    prompt=input_prompt,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    eta=eta,
                    negative_prompt=negative_prompt,
                    generator=randomSeeds[step],
                )

                current_images[step] = generated.images[0]

                file_number += 1

                file_path = os.path.join(
                    save_folder, f"{date_prefix}.png"
                )
                current_images[step].save(file_path)

                self.progress = step + 1

                elapsed_time = time.time() - start_time
                if step > 0:
                    average_time_per_step = elapsed_time / step
                    remaining_steps = num_inference_steps - step
                    estimated_time = average_time_per_step * remaining_steps
                    self.estimated_time = round(estimated_time, 2)

            self.generation_complete = True

            if batch_size > 1:
                grid_size = math.ceil(math.sqrt(batch_size))
                generated_images = self.image_grid(
                    current_images, grid_size, grid_size, max_size=512
                )
                save_path = os.path.join(save_folder, f"{date_prefix}.png")
                generated_images.save(save_path)
                print(f"Image saved at: {save_path}")

            final_file_number = date_prefix

            return save_folder, final_file_number
