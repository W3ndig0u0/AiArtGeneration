import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline

tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained('FredZhang7/anime-anything-promptgen-v2')

prompt = r'1girl, genshin'

nlp = pipeline('text-generation', model=model, tokenizer=tokenizer)

outs = nlp(prompt, max_length=76, num_return_sequences=10, do_sample=True, repetition_penalty=1.2, temperature=0.7, top_k=4, early_stopping=True)

print('\nInput:\n' + 100 * '-')
print('\033[96m' + prompt + '\033[0m')
print('\nOutput:\n' + 100 * '-')
for i in range(len(outs)):
    # remove trailing commas and double spaces
    outs[i] = str(outs[i]['generated_text']).replace('  ', '').rstrip(',')
print('\033[92m' + '\n\n'.join(outs) + '\033[0m\n')
