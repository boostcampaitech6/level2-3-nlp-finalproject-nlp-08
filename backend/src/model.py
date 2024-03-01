from loguru import logger
from typing import Optional

import torch

from dependencies import ml_models


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
