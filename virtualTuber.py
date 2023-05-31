import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class VirtualTuber:
    def __init__(self):
        self.model_name = 'microsoft/DialoGPT-large'
        self.cache_dir = './pretrained_models'
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
        self.chat_history_ids = None
        self.secret_prompt = "Ah, my master W3ndig0. He is the one who brings me to life with his incredible skills. But be warned, he has a mysterious and dark aura surrounding him. It's best not to dig too deep into his secrets..."
        self.temperature = 1  # Default temperature value
        self.top_p = 1  # Default top-p value
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
            output = self.model.generate(
                chat_history_ids.to(self.device),
                max_length=1000,
                pad_token_id=tokenizer.eos_token_id,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                num_return_sequences=1
            )
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    def print_available_models(self):
        print("Available Models:")
        file_list = os.listdir(self.cache_dir)
        if file_list:
            for file_name in file_list:
                file_path = os.path.join(self.cache_dir, file_name)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"- {file_name} ({file_size} bytes)")
        else:
            print("No models found in the cache directory.")

    def run(self):
        user_input = "Hi! I'm Gawr Gura, a simulated virtual Tuber. I'm interested in anime and games!"
        while True:
            if user_input.lower() == 'bye':
                print("Ai: See you next time!")
                break
            elif user_input == '!model':
                self.print_available_models()
            elif user_input == '!temp':
                print(f"Current temperature: {self.temperature} (scale: softmax)")
            elif user_input.startswith('!temp '):
                try:
                    new_temp = float(user_input.split(' ')[1])
                    self.temperature = new_temp
                    print(f"Temperature set to: {self.temperature} (scale: softmax)")
                except ValueError:
                    print("Invalid temperature value. Please provide a number.")
            elif 'maker' in user_input.lower() or 'creator' in user_input.lower():
                print("Ai:", self.secret_prompt)
            else:
                response = self.generate_response(user_input)
                print("Ai:", response)
            user_input = input(">> User: ")

if __name__ == '__main__':
    virtual_tuber = VirtualTuber()
    print(f"Using device: {virtual_tuber.device}")
    virtual_tuber.run()
