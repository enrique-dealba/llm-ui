from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from agent_files.objectives import kv_objectives

def get_embedding_fn(model_name: str = 'thenlper/gte-small'):
    model = SentenceTransformer(model_name)
    assert model is not None
    embedding_fn = lambda x: model.encode(x)
    return embedding_fn

def get_objective(task: str, embedding_fn):
    assert kv_objectives is not None
    task_emb = embedding_fn(task)

    max_cos_sim = -1
    objective = None
    for key_desc, value in kv_objectives.items():
        key_emb = embedding_fn(key_desc)
        cosine_sim = cos_sim(task_emb, key_emb)
        if cosine_sim > max_cos_sim:
            max_cos_sim = cosine_sim
            objective = value
            
    assert objective is not None
    return objective
