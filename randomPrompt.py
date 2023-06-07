import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline


def prompt():
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    model = GPT2LMHeadModel.from_pretrained("FredZhang7/anime-anything-promptgen-v2")

    prompt = r"best quality, ultra detailed, 1girl, solo, stunning background, genshin"

    nlp = pipeline("text-generation", model=model, tokenizer=tokenizer)

    outs = nlp(
        prompt,
        max_length=76,
        num_return_sequences=1,
        do_sample=True,
        repetition_penalty=1.2,
        temperature=0.7,
        top_k=4,
    )

    for i in range(len(outs)):
        outs[i] = str(outs[i]["generated_text"]).replace("  ", "").rstrip(",")
    return outs
