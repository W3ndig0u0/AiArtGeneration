from transformers import AutoModelForCausalLM, AutoTokenizer, CLIPTextConfig
from diffusers import StableDiffusionPipeline
from diffusers.models import AutoencoderKL
import torch
import os


def load_modelDiff(model_name, vae_name, cache_dir, device):
    """Load a Stable Diffusion model with a specified VAE."""
    var_cache_dir = os.path.join("ArtVae")
    
    vae = AutoencoderKL.from_pretrained(
        vae_name, 
        torch_dtype=torch.float16, 
        cache_dir=var_cache_dir
    )

    print(f"Using {model_name} NOW!")

    load_method = (
        StableDiffusionPipeline.from_ckpt if model_name.endswith((".safetensors", ".ckpt")) 
        else StableDiffusionPipeline.from_pretrained
    )

    model = load_method(
        model_name,
        cache_dir=cache_dir,
        torch_dtype=torch.float16, 
        vae=vae,
        local_files_only=True,
        safety_checker=None,       
        requires_safety_checker=False,
        low_cpu_mem_usage=False, 
    )

    model.to(device)

    if device in ["cuda", "mps"]:
        if device == "cuda":
            model.enable_xformers_memory_efficient_attention()
        else:
            torch.backends.mps.enable_xformers_memory_efficient_attention()

    return model
