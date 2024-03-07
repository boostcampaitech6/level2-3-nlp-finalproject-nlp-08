from keybert import KeyBERT
import pandas as pd
import re
from transformers import BertModel
from collections import defaultdict

def keyword_extraction(context, kw_model, num_to_gen = 5, stop_words = None, n_gram = 5, use_maxsum=True, nr_candidates=10):
    
    keywords = kw_model.extract_keywords(context, 
                                      keyphrase_ngram_range=(1, n_gram), 
                                      stop_words=stop_words, 
                                      top_n=num_to_gen)
    keywords = [k[0] for k in keywords]

    return keywords