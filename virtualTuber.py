import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from fileSize import print_available_models, get_folder_size, convert_size
from loadModel import load_model


class VirtualTuber:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-large"
        self.cache_dir = "./languageModel"
        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        self.chat_history_ids = None
        self.secret_prompt = "Ah, my master W3ndig0. He is the one who brings me to life with his incredible skills. But be warned, he has a mysterious and dark aura surrounding him. It's best not to dig too deep into his secrets..."
        self.load_model()

    def load_model(self):
        self.model, tokenizer = load_model(self.model_name, self.cache_dir, self.device)

    def generate_response(self, user_input):
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
        elif torch.cuda.is_available():
            torch.cuda.empty_cache()

        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir, padding_side="left"
        )
        user_input_ids = tokenizer.encode(
            user_input + tokenizer.eos_token, return_tensors="pt"
        )
        chat_history_ids = (
            torch.cat([self.chat_history_ids, user_input_ids], dim=-1)
            if self.chat_history_ids is not None
            else user_input_ids
        )
        with torch.no_grad():
            self.model.config.encoder_no_repeat_ngram_size = None
            response_ids = self.model.generate(
                chat_history_ids.to(self.device),
                max_length=1000,
                pad_token_id=tokenizer.eos_token_id,
            )
        response = tokenizer.decode(
            response_ids[:, chat_history_ids.shape[-1] :][0], skip_special_tokens=True
        )
        return response

    def run(self, user_input):
        response = ""
        if "!model" in user_input.lower():
            response = print_available_models(self.cache_dir)
        elif "maker" in user_input.lower() or "creator" in user_input.lower():
            response = self.secret_prompt
        else:
            response = self.generate_response(user_input)
        return response
