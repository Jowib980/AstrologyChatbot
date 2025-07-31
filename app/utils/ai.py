from openai import OpenAI
import os
from app.utils.astrology import get_zodiac_positions
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

model_path = "./models/final-astro-model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def format_prompt(name, dob, time, place, question):
    planetary = get_zodiac_positions(dob, time, place)
    if not isinstance(planetary, dict):
        return None

    planet_str = ", ".join([f"{planet} in {sign}" for planet, sign in planetary.items()])

    return (
        f"{name} was born on {dob} at {time} in {place}. "
        f"The planetary positions were: {planet_str}. "
        f"Their question is: \"{question}\". "
        f"Please provide a helpful and personalized astrology-based answer."
    )

def generate_answer(prompt):
    print(prompt)
    # try:
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are an expert astrologer giving personalized answers based on birth chart details."},
    #             {"role": "user", "content": prompt}
    #         ],
    #         temperature=0.7,
    #         max_tokens=500,
    #         top_p=0.95
    #     )
    #     return response.choices[0].message.content.strip()

    # except Exception as e:
    #     print("OpenAI error:", e)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            num_beams=4,
            early_stopping=True, 
            do_sample=False,
            num_return_sequences=1,
            max_new_tokens=200,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
