from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from app.utils.astrology import get_zodiac_positions

model_path = "./models/final-astro-model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

def format_prompt(name, dob, time, place, question):
    planetary = get_zodiac_positions(dob, time, place)

    if not isinstance(planetary, dict):
        return None  # or return a fallback prompt string if desired

    planet_str = ", ".join([f"{planet} in {sign}" for planet, sign in planetary.items()])
    
    return f"{name} was born on {dob} at {time} in {place}. The planetary positions were: {planet_str}. The question is: {question}"


def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=128,
            num_beams=4,
            early_stopping=True, 
            temperature=0.9,
            top_k=50,
            top_p=0.95,
            num_return_sequences=1,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
