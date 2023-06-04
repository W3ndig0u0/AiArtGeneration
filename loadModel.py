from transformers import AutoModelForCausalLM, AutoTokenizer, CLIPTextConfig
from diffusers import StableDiffusionPipeline
import torch
import os

# model = None  # Global variable to store the loaded model
# vae = None  # Global variable to store the loaded VAE model


def load_model(model_name, cache_dir, device):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, cache_dir=cache_dir, padding_side="left"
    )

    model_path = os.path.join(cache_dir, model_name)
    if not os.path.exists(model_path):
        print("Using " + model_name)
        model = AutoModelForCausalLM.from_pretrained(model_path, cache_dir=cache_dir)
    else:
        print("The model is already downloaded.")
        model = AutoModelForCausalLM.from_pretrained(model_path, cache_dir=cache_dir)

    model.to(device)
    return model, tokenizer


# def load_modelDiff(model_name, cache_dir, device):
#     # global model, vae

#     if model is None:
#         model_path = os.path.join(cache_dir, model_name)
#         if not os.path.exists(model_path):
#             print("DOWNLOADING " + model_name + " NOW!")
#             model = StableDiffusionPipeline.from_pretrained(
#                 model_name,
#                 cache_dir=cache_dir,
#                 torch_dtype=torch.float16,
#             )
#         else:
#             print("The model is already downloaded.")
#             model = StableDiffusionPipeline.from_pretrained(
#                 model_name,
#                 cache_dir=cache_dir,
#                 torch_dtype=torch.float16,
#             )

#     # if vae is None:
#     #     vae_filepath = "ArtVae/pastel-waifu-diffusion.vae.pt"
#     #     vae = torch.load(vae_filepath, map_location=torch.device("mps"))

#     # model.vae = vae

#     model = model.to(device)
#     return model


def load_modelDiff(model_name, cache_dir, device):
    model_path = os.path.join(cache_dir, model_name)
    if not os.path.exists(model_path):
        print("DOWNLOADING " + model_name + " NOW!")
        model = StableDiffusionPipeline.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
        )
    else:
        print("The model is already downloaded.")
        model = StableDiffusionPipeline.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
        )

    model = model.to(device)
    return model
