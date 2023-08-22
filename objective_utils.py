import json
import os
import re
import torch
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

def calculate_confidence(distribution: List[float]):
    """
    Calculates the confidence of a given distribution based on entropy. The 
    function normalizes the distribution, computes the entropy, and then 
    normalizes it considering the maximum entropy for the given length. It's 
    useful for assessing the uncertainty or randomness associated with a 
    particular distribution, returning the confidence level as a percentage.
    """
    if not distribution:
        return 0
        
    if str(type(distribution[0])) == "<class 'torch.Tensor'>":
        new_dist = [sim.item() for sim in distribution]
        distribution = new_dist
    # Normalizes the distribution so that it sums to 1
    distribution = np.array(distribution) / sum(distribution)
    # Calculates entropy
    entropy = -np.sum(distribution * np.log2(distribution))
    # Normalizes entropy to the range [0, 1], considering max entropy for given length
    max_entropy = np.log2(len(distribution))
    confidence = 1 - (entropy / max_entropy)
    return confidence * 100

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
