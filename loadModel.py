from transformers import AutoModelForCausalLM, AutoTokenizer, CLIPTextConfig
from diffusers import StableDiffusionPipeline
from diffusers.models import AutoencoderKL
import torch
import os


def load_model(model_name, cache_dir, device):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, cache_dir=cache_dir, padding_side="left"
    )

    print("Using " + model_name)
    model = AutoModelForCausalLM.from_pretrained(model_path, cache_dir=cache_dir)
    model.to(device)
    return model, tokenizer


def load_modelDiff(model_name, vae_name, cache_dir, device):
    var_cache_dir = os.path.join("ArtVae")
    safe_cache_dir = os.path.join("artModel")
    vae = AutoencoderKL.from_pretrained(
        vae_name, torch_dtype=torch.float16, cache_dir=var_cache_dir
    )

    print("Using " + model_name + " NOW!")
    if model_name.endswith(".safetensors") or model_name.endswith(".ckpt"):
        model = StableDiffusionPipeline.from_ckpt(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
            vae=vae,
            local_files_only=True,
        )
    else:
        model = StableDiffusionPipeline.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
            vae=vae,
            local_files_only=True,
        )

    print("Using " + model_name + " NOW!")
    model = StableDiffusionPipeline.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        torch_dtype=torch.float16,
        vae=vae,
        local_files_only=True,
        use_safetensors=True,
    )

    model = model.to(device)
    if device == "cuda":
        model.enable_xformers_memory_efficient_attention()
    elif device == "mps":
        torch.backends.mps.enable_xformers_memory_efficient_attention()

    return model
