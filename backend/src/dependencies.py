from keybert import KeyBERT
from transformers import (
    PreTrainedTokenizerFast, BertModel, BartForConditionalGeneration
)

ml_models = {}

def load_qg_model():
    global ml_models

    ml_models['tokenizer'] = PreTrainedTokenizerFast.from_pretrained('Sehong/kobart-QuestionGeneration')
    ml_models["qg_model"] = BartForConditionalGeneration.from_pretrained('Sehong/kobart-QuestionGeneration')
    ml_models['ke_model'] = KeyBERT(BertModel.from_pretrained('skt/kobert-base-v1'))

    return ml_models


