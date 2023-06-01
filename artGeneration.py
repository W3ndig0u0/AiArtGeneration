import torch
from PIL import Image
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
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
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def generate_art(
        self,
        prompt,
        height,
        width,
        num_inference_steps,
        eta,
        guidance_scale,
        save_folder,
        initial_generation=False,
        seed=None,
        batch_size=1,
    ):
        if initial_generation:
            self.progress = 0
        self.total_steps = num_inference_steps
        self.generation_complete = False
        self.estimated_time = None

        if self.generator is None:
            model_folder = "./artModel"
            model_id = "stablediffusionapi/anime-model-v2"
            model_file, _ = load_modelDiff(model_id, model_folder, self.device)

            self.generator = DiffusionPipeline.from_pretrained(model_file)
            self.generator.scheduler = DPMSolverMultistepScheduler.from_config(
                self.generator.scheduler.config
            )
            self.generator.enable_attention_slicing()

        with torch.no_grad():
            generator = self.generator.to(self.device)
            current_images = [None] * batch_size
            intermediate_folder = os.path.join(save_folder, "intermediate")

            os.makedirs(intermediate_folder, exist_ok=True)

            existing_files = os.listdir(intermediate_folder)
            file_count = len(existing_files)
            randomSeed = [
                torch.Generator(self.device).manual_seed(seed)
                for _ in range(batch_size)
            ]

            for step in range(num_inference_steps):
                generated = generator(
                    prompt=prompt,
                    height=height,
                    width=width,
                    num_inference_steps=1,
                    eta=eta,
                    guidance_scale=guidance_scale,
                    generator=randomSeed,
                )

                current_images = generated.images

                for i, image in enumerate(current_images):
                    file_number = file_count + step * batch_size + i + 1
                    save_path = os.path.join(intermediate_folder, f"{file_number}.png")
                    image.save(save_path)

                self.progress = step + 1
                time.sleep(1)

            final_file_number = file_count + num_inference_steps * batch_size
            final_save_path = os.path.join(
                save_folder, f"{final_file_number}-final.png"
            )

            current_images[-1].save(final_save_path)

            self.generation_complete = True

        return intermediate_folder, final_save_path


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
        eta,
        guidance_scale,
        save_folder,
        initial_generation=False,
        seed=seed,
        batch_size=batch_size,
    )
