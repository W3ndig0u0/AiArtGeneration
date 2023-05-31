import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class VirtualTuber:
    def __init__(self):
        self.model_name = 'microsoft/DialoGPT-large'
        self.cache_dir = './pretrained_models'
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.chat_history_ids = None
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
        for root, dirs, files in os.walk(self.cache_dir):
            for file in files:
                if file.endswith(".bin"):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    print(f"- {file} ({file_size} bytes)")

    def run(self):
        while True:
            user_input = input(">> User: ")
            if user_input.lower() == 'bye':
                print("Ai: See you next time!")
                break
            if user_input.lower() == '!models':
                self.print_available_models()
                continue
            response = self.generate_response(user_input)
            print("Ai:", response)


if __name__ == "__main__":
    tuber = VirtualTuber()
    tuber.run()
