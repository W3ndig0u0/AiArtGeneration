import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

dataset = [
    {"user_input": "Hello",
        "gawr_gura_response": "Hello, I'm Gawr Gura! How can I help you today?"},
    {"user_input": "Tell me a Shark Fact",
        "gawr_gura_response": "Did you know that sharks have been around for millions of years?"}
]

model_name = 'microsoft/DialoGPT-large'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

training_args = TrainingArguments(
    output_dir='./fine_tuned_model',
    num_train_epochs=1,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
)


def data_collator(data):
    inputs = tokenizer(data["user_input"], padding="max_length",
                       truncation=True, max_length=512, return_tensors="pt")
    inputs["labels"] = tokenizer(data["gawr_gura_response"], padding="max_length",
                                 truncation=True, max_length=512, return_tensors="pt")["input_ids"]
    return inputs


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
)

trainer.train()
