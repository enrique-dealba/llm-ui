import json
import os
import re
import numpy as np

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from typing import List

from agent_files.objectives import kv_objectives


def get_embedding_fn(model_name: str = 'thenlper/gte-small'):
    model = SentenceTransformer(model_name)
    assert model is not None
    embedding_fn = lambda x: model.encode(x)
    return embedding_fn

def calculate_confidence(cosine_similarities: List[float]):
    """
    Takes an array of cosine similarities as input and calculates a confidence 
    percentage based on the distribtion of cosine similarities.
    """
    max_similarity = np.max(cosine_similarities)
    mean = np.mean(cosine_similarities)
    std = np.std(cosine_similarities)

    # Compute the confidence percentage
    confidence_percentage = (max_similarity - mean) / std
    confidence_percentage = max(0, min(1, confidence_percentage)) * 100

    return confidence_percentage

def get_objective(task: str, embedding_fn = None):
    assert kv_objectives is not None
    if embedding_fn is None:
        embedding_fn = get_embedding_fn()
    task_emb = embedding_fn(task)

    max_cos_sim = -1
    objective = None
    cosine_sims = []
    for key_desc, value in kv_objectives.items():
        key_emb = embedding_fn(key_desc)
        cosine_sim = cos_sim(task_emb, key_emb)
        cosine_sims.append(cosine_sim)
        if cosine_sim > max_cos_sim:
            max_cos_sim = cosine_sim
            objective = value
            
    assert objective is not None
    confidence_value = calculate_confidence(cosine_sims)
    return objective, confidence_value

def save_json(json_file,
              directory: str = 'agent_objectives',
              filename: str = 'objective.json'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = os.path.join(directory, filename)

    with open(path, 'w') as file:
        json.dump(json_file, file, indent=4)

    print(f"Saved JSON object to {path}")

def extract_json(input_string: str):
    match = re.search(r'\{.*?\}', input_string, re.DOTALL)
    if match:
        # Extracts the JSON object
        json_text = match.group(0)

        # Removes extra whitespaces and newlines
        json_text = re.sub(r'\s+', ' ', json_text).strip()

        return json_text
    else:
        raise ValueError("JSON object not found in the input string")
