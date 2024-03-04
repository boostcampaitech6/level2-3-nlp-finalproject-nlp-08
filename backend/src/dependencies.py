
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

ml_models = {}

def load_qg_model():
    global ml_models

    ml_models['tokenizer'] = PreTrainedTokenizerFast.from_pretrained('Sehong/kobart-QuestionGeneration')
    ml_models["qg_model"] = BartForConditionalGeneration.from_pretrained('Sehong/kobart-QuestionGeneration')
    
    return ml_models


