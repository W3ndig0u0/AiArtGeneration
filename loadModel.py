from transformers import AutoModelForCausalLM, AutoTokenizer
from diffusers import DiffusionPipeline
import torch
import os
from flask import Flask, render_template, request, jsonify


def load_model(model_name, cache_dir, device):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, cache_dir=cache_dir, padding_side="left"
    )

    model_path = os.path.join(cache_dir, model_name)
    if not os.path.exists(model_path):
        print("ERROR: THE MODEL IS NOT DOWNLOADED.")
        print("DOWNLOADING " + model_name + " NOW!")
        model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)
    else:
        print("The model is already downloaded.")
        model = AutoModelForCausalLM.from_pretrained(model_path, cache_dir=cache_dir)

    model.to(device)
    torch.cuda.empty_cache()
    return model, tokenizer


def load_modelDiff(model_name, cache_dir, device):
    model_path = os.path.join(cache_dir, model_name)
    if not os.path.exists(model_path):
        print("DOWNLOADING " + model_name + " NOW!")
        model = DiffusionPipeline.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
        )
    else:
        print("The model is already downloaded.")
        model = DiffusionPipeline.from_pretrained(
            model_name,
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
        )
    model = model.to(device)
    torch.cuda.empty_cache()
    return model
