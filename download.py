import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = 'EleutherAI/gpt-j-6b'
cache_dir = './pretrained_models'

tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, padding_side='left')

try:
    model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)
    print("The model is already downloaded.")
except OSError:
    # If model is not downloaded, download it
    print("ERROR: THE MODEL IS NOT DOWNLOADED.")
    print("DOWNLOADING " + model_name + " NOW!")
    model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if torch.cuda.is_available():
    torch.cuda.set_device(torch.cuda.current_device())
    print("Using GPU:", torch.cuda.get_device_name())
else:
    print("Using CPU")
model.to(device)

MAX_HISTORY_LENGTH = 5
chat_history_ids = None

while True:
    user_input = input(">> User: ")
    if user_input.lower() == 'bye':
        print("Ai: Goodbye!")
        break

    if user_input.lower() == '!models':
        # Print all models in the cache directory
        print("Available Models:")
        for filename in os.listdir(cache_dir):
            if filename.endswith(".bin"):
                file_path = os.path.join(cache_dir, filename)
                file_size = os.path.getsize(file_path)
                print(f"- {filename} ({file_size} bytes)")
        continue

    # Encode the new user input and add eos_token
    user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Update the chat history with the new user input
    chat_history_ids = torch.cat([chat_history_ids, user_input_ids], dim=-1) if chat_history_ids is not None else user_input_ids

    # Generate a response
    with torch.no_grad():
        model.config.encoder_no_repeat_ngram_size = None  # Disable encoder_no_repeat_ngram_size
        response_ids = model.generate(chat_history_ids.to(device), max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Decode and print the response
    response = tokenizer.decode(response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
    print("Ai:", response)
