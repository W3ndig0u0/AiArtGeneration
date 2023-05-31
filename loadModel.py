import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_name, cache_dir, device):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, cache_dir=cache_dir, padding_side='left')
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name, cache_dir=cache_dir)
        print("The model is already downloaded.")
    except OSError:
        print("ERROR: THE MODEL IS NOT DOWNLOADED.")
        print("DOWNLOADING " + model_name + " NOW!")
        model = AutoModelForCausalLM.from_pretrained(
            model_name, cache_dir=cache_dir)
    model.to(device)
    return model, tokenizer
