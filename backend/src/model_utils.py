from loguru import logger
from typing import Optional, List

import torch
import re
from kiwipiepy import Kiwi

from dependencies import ml_models

def extract_keywords(context: str, num_to_gen: int) -> List[str]:
    model = ml_models['ke_model']
    keywords = model.extract_keywords(context, 
                                      keyphrase_ngram_range=(1, 1), 
                                      stop_words=None, 
                                      top_n=num_to_gen,
                                      use_mmr=True,
                                      diversity=0.1)

    keywords = [k[0] for k in keywords]
    keywords = [extracts_nouns(i) for i in keywords if extracts_nouns(i) != None and extracts_nouns(i) in context]

    return keywords


def generate_question(context: str, answer: Optional[str]) -> str:
    max_encoded_context_len = 1000
    tokenizer = ml_models['tokenizer']
    model = ml_models['qg_model']

    raw_input_context = tokenizer.encode(context)
    raw_input_rest = tokenizer.encode('<unused0>' + answer)
    raw_input_ids = raw_input_context[:max_encoded_context_len] + raw_input_rest
    
    logger.debug(f"raw input context size={len(raw_input_context)}")
    
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
    logger.debug(f"model input text {context} + {'<unused0>'} + {answer}")
    summary_ids = model.generate(torch.tensor([input_ids]))
    generated_question = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

    return generated_question

def extracts_nouns(keyword):
    kiwi = Kiwi()
    final_keyword = []
    for k in keyword.split():
        temp_keyword = ''
        for i in kiwi.tokenize(k):
            if i.tag.startswith('N') or i.tag=='SN' and i.tag !='NP':
                temp_keyword += i.form
        final_keyword.append(temp_keyword)
    if len(final_keyword) != 0:
        return ' '.join(final_keyword)