import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class VirtualTuber:
    def __init__(self):
        self.model_name = 'microsoft/DialoGPT-large'
        self.cache_dir = './pretrained_models'
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.chat_history_ids = None
        self.secret_prompt = "Ah, my master W3ndig0. He is the one who brings me to life with his incredible skills. But be warned, he has a mysterious and dark aura surrounding him. It's best not to dig too deep into his secrets..."
        self.load_model()

    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir, padding_side='left')
        try:
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            print("The model is already downloaded.")
        except OSError:
            print("ERROR: THE MODEL IS NOT DOWNLOADED.")
            print("DOWNLOADING " + self.model_name + " NOW!")
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        self.model.to(self.device)

    def generate_response(self, user_input):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir, padding_side='left')
        user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = torch.cat([self.chat_history_ids, user_input_ids], dim=-1) if self.chat_history_ids is not None else user_input_ids
        with torch.no_grad():
            self.model.config.encoder_no_repeat_ngram_size = None
            response_ids = self.model.generate(chat_history_ids.to(self.device), max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

    def print_available_models(self):
        print("Available Models:")
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".bin"):
                file_path = os.path.join(self.cache_dir, filename)
                file_size = os.path.getsize(file_path)
                print(f"- {filename} ({file_size} bytes)")

    def run(self):
        user_input = "Hi! I'm Gawr Gura, a simulated virtual Tuber. I'm interested in anime and games. Let's chat!"
        while True:
            if user_input.lower() == 'bye':
                print("Ai: See you next time!")
                break
            if 'maker' in user_input.lower() or 'creator' in user_input.lower():
                print("Ai:", self.secret_prompt)
            else:
                response = self.generate_response(user_input)
                print("Ai:", response)
            user_input = input(">> User: ")

