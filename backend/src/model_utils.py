from loguru import logger
from typing import Optional, List

import torch

from dependencies import ml_models

def extract_keywords(context: str, num_to_gen: int) -> List[str]:
    model = ml_models['ke_model']

    keywords = model.extract_keywords(context, 
                                      keyphrase_ngram_range=(1, 2), 
                                      stop_words=None, 
                                      top_n=num_to_gen)
    keywords = [k[0] for k in keywords]

    return keywords


def generate_question(context: str, answer: Optional[str]) -> str:
    tokenizer = ml_models['tokenizer']
    model = ml_models['qg_model']

    raw_input_text = context + '<unused0>' + answer
    raw_input_ids = tokenizer.encode(raw_input_text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
    logger.debug(f"model input text {raw_input_text}")
    summary_ids = model.generate(torch.tensor([input_ids]))
    generated_question = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

    return generated_question
