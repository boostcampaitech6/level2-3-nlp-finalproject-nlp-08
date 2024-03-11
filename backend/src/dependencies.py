from yaml import load, FullLoader

from keybert import KeyBERT
from transformers import (
    PreTrainedTokenizerFast, BertModel, BartForConditionalGeneration
)

ml_models = {}

def load_qg_model(tokenizer, qg_model, ke_model):
    global ml_models

    ml_models['tokenizer'] = PreTrainedTokenizerFast.from_pretrained(tokenizer)
    ml_models["qg_model"] = BartForConditionalGeneration.from_pretrained(qg_model)
    ml_models['ke_model'] = KeyBERT(BertModel.from_pretrained(ke_model))

    return ml_models


def load_config(config_path):
    with open(config_path, "r") as f:
        config = load(f, FullLoader)
    
    return config