import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from fileSize import print_available_models, get_folder_size, convert_size
from loadModel import load_model

class VirtualTuber:
    def __init__(self):
        self.model_name = 'microsoft/DialoGPT-large'
        self.cache_dir = './languageModel'
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.secret_prompt = "Ah, my master W3ndig0. He is the one who brings me to life with his incredible skills. But be warned, he has a mysterious and dark aura surrounding him. It's best not to dig too deep into his secrets..."
        self.load_model()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir, padding_side='left')
        self.chat_history = []

    def load_model(self):
        self.model, _ = load_model(self.model_name, self.cache_dir, self.device)

    def generate_response(self, user_input):
        user_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = torch.cat([self.chat_history, user_input_ids], dim=-1) if self.chat_history else user_input_ids
        with torch.no_grad():
            self.model.config.encoder_no_repeat_ngram_size = None
            response_ids = self.model.generate(chat_history_ids.to(self.device), max_length=1000, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

    def run(self, user_input):
        response = ''
        if '!model' in user_input.lower():
            response = print_available_models(self.cache_dir)
        elif 'maker' in user_input.lower() or 'creator' in user_input.lower():
            response = self.secret_prompt
        else:
            response = self.generate_response(user_input)
            # Maintain chat history
            self.chat_history.append(response)
            self.chat_history = self.chat_history[-3:]  # Store only the last 3 exchanges
        return response

if __name__ == '__main__':
    virtual_tuber = VirtualTuber()
    print(f"Using device: {virtual_tuber.device}")
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break
        response = virtual_tuber.run(user_input)
        print("VirtualTuber:", response)
