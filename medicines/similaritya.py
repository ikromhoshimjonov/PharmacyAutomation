import os
import numpy as np
from openai import OpenAI


SECRET_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=SECRET_KEY)

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def get_embedding(name, description=""):
    try:
        print(description)
        clean_name = name.replace("Forte", "").replace("Neo", "").strip()
        rich_text = f"Vazifasi: {description}. Dori: {clean_name}"

        response = client.embeddings.create(
            input=[rich_text.replace("\n", " ")],
            model="text-embedding-3-small"
        )
        return np.array(response.data[0].embedding, dtype=np.float32)
    except Exception as e:
        print(f"OpenAI error: {e}")
        return None