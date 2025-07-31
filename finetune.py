from datasets import load_dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq
import torch

# Load dataset
dataset = load_dataset("json", data_files="astro_dataset.json")

# Load tokenizer and model
base_model = "google/flan-t5-small"
tokenizer = T5Tokenizer.from_pretrained(base_model)
model = T5ForConditionalGeneration.from_pretrained(base_model)

# Preprocessing function
def preprocess(example):
    model_inputs = tokenizer(example["input"], truncation=True, padding="max_length", max_length=128)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(example["output"], truncation=True, padding="max_length", max_length=128)

    # Replace pad token id with -100 so loss is ignored on those tokens
    labels["input_ids"] = [
        (label if label != tokenizer.pad_token_id else -100) for label in labels["input_ids"]
    ]
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


tokenized_dataset = dataset["train"].map(preprocess)

# Training setup
training_args = TrainingArguments(
    output_dir="./models/final-astro-model",
    per_device_train_batch_size=4,
    num_train_epochs=5,
    logging_dir="./logs",
    save_total_limit=1,
    save_strategy="epoch",
    fp16=torch.cuda.is_available()
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model)
)

# Train and save
trainer.train()
model.save_pretrained("./models/final-astro-model")
tokenizer.save_pretrained("./models/final-astro-model")
