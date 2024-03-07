from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import torch.nn as nn

class lcw(nn.Module):
    def __init__(self):
        nltk.download('punkt')
        super().__init__()
        self.model_dir = model_dir = "lcw99/t5-base-korean-text-summary"
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.max_input_length = 512

    def forward(self, list_full_texts):
        inputs = ["summarize: " + text for text in list_full_texts]

        inputs = self.tokenizer(inputs, max_length=self.max_input_length, truncation=True, return_tensors="pt")
        output = self.model.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=100)
        decoded_output = self.tokenizer.batch_decode(output, skip_special_tokens=True)
        list_predicted_titles = [nltk.sent_tokenize(decoded.strip())[0] for decoded in decoded_output]
        return list_predicted_titles
