import os
import torch
import math
from transformers import AutoTokenizer, AutoModelForCausalLM

class VirtualTuber:
    def __init__(self):
        self.model_name = 'microsoft/DialoGPT-large'
        self.cache_dir = './languageModel'
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.chat_history_ids = None
        self.secret_prompt = "Ah, my master W3ndig0. He is the one who brings me to life with his incredible skills. But be warned, he has a mysterious and dark aura surrounding him. It's best not to dig too deep into his secrets..."
        self.load_model()

    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir, padding_side='left')
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name, cache_dir=self.cache_dir)
            print("The model is already downloaded.")
        except OSError:
            print("ERROR: THE MODEL IS NOT DOWNLOADED.")
            print("DOWNLOADING " + self.model_name + " NOW!")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name, cache_dir=self.cache_dir)
        self.model.to(self.device)

    def generate_response(self, user_input):
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir, padding_side='left')
        user_input_ids = tokenizer.encode(
            user_input + tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = torch.cat([self.chat_history_ids, user_input_ids],
                                     dim=-1) if self.chat_history_ids is not None else user_input_ids
        with torch.no_grad():
            self.model.config.encoder_no_repeat_ngram_size = None
            response_ids = self.model.generate(chat_history_ids.to(
                self.device), max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(
            response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

    def print_available_models(self):
        file_list = os.listdir(self.cache_dir)
        if file_list:
            response = ""
            for file_name in file_list:
                file_path = os.path.join(self.cache_dir, file_name)
                if os.path.isdir(file_path):
                    file_size = get_folder_size(file_path)
                    response += f"{file_name} ({file_size})"
        else:
            response = "No models found in the cache directory."
        return response


    def run(self, user_input):
        response = ''
        if '!model' in user_input.lower():
            response = self.print_available_models()
        elif 'maker' in user_input.lower() or 'creator' in user_input.lower():
            response = self.secret_prompt
        else:
            response = self.generate_response(user_input)
        return response

if __name__ == '__main__':
    virtual_tuber = VirtualTuber()
    print(f"Using device: {virtual_tuber.device}")
    virtual_tuber.run()

def get_folder_size(folder_path):
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)
    return convert_size(total_size)

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_bytes / p, 2)
    return f"{size} {size_name[i]}"
