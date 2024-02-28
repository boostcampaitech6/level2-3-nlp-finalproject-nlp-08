from dataclass import DocumentOut, DocumentIn, doc_in_ex, doc_out_ex

from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration


def load_qg_model():
    print("load model and tokenizer")
    tokenizer = PreTrainedTokenizerFast.from_pretrained('Sehong/kobart-QuestionGeneration')
    model = BartForConditionalGeneration.from_pretrained('Sehong/kobart-QuestionGeneration')
    
    return tokenizer, model
    


