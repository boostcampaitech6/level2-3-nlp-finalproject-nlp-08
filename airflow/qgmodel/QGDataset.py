import pandas as pd
import numpy as np
import torch
from datasets import load_dataset

from transformers import AutoTokenizer

class QGDataset(torch.utils.data.Dataset):
    def __init__(self, dataset_name, tokenizer_name, input_max_len, model_type, train=True, token=None, ignore_index=-100):
        
        if dataset_name[-3:] == 'csv':
            self.dataset = pd.read_csv(dataset_name)  
        else:
            self.dataset = load_dataset(dataset_name, token=token)  
            if train == True:
                self.dataset = self.dataset['train'].to_pandas()[:5]
            else:
                self.dataset = self.dataset['test'].to_pandas()[:5]

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.tokenizer.sep_token = '<unused0>'
        
        self.input_max_len = input_max_len
        self.pad_index = self.tokenizer.pad_token_id
        self.ignore_index = ignore_index
        self.model_type = model_type
        
        self.len = len(self.dataset)


    def add_padding_data(self, inputs):
        if len(inputs) < self.input_max_len:
            pad = np.array([self.pad_index] * (self.input_max_len - len(inputs)))
            inputs = np.concatenate([inputs, pad])
        else:
            inputs = inputs[:self.input_max_len]

        return inputs
    
    def add_ignored_data(self, inputs):
        if len(inputs) < self.input_max_len:
            pad = np.array([self.ignore_index] * (self.input_max_len - len(inputs)))
            inputs = np.concatenate([inputs, pad])
        else:
            inputs = inputs[:self.input_max_len]

        return inputs
    
    def __getitem__(self, idx):
        instance = self.dataset.iloc[idx]

        if self.model_type == 'BART':
            tokenized_input = self.tokenizer(instance['context'] + self.tokenizer.sep_token + instance['answer'], 
                                             max_length=self.input_max_len, 
                                             padding="max_length",
                                             truncation=True)
            input_ids = tokenized_input['input_ids']
            attention_mask = tokenized_input['attention_mask']

            label_ids = self.tokenizer.encode(instance['question'])
            label_ids.append(self.tokenizer.eos_token_id)
            dec_input_ids = [self.tokenizer.eos_token_id]
            dec_input_ids += label_ids[:-1]
            dec_input_ids = self.add_padding_data(dec_input_ids)
            label_ids = self.add_ignored_data(label_ids)

            decoder_attention_mask = (dec_input_ids != self.pad_index)

        elif self.model_type == 'T5':
            tokenized_input = self.tokenizer('answer:' + instance['answer'] + 'content:' + instance['context'], 
                                             max_length=self.input_max_len, 
                                             padding="max_length",
                                             truncation=True)
            input_ids = tokenized_input['input_ids']
            attention_mask = tokenized_input['attention_mask']

            label_ids = self.tokenizer.encode('question:' + instance['question'], add_special_tokens=False)
            label_ids.append(self.tokenizer.eos_token_id)
            dec_input_ids = [self.tokenizer.eos_token_id]
            dec_input_ids += label_ids[:-1]
            dec_input_ids = self.add_padding_data(dec_input_ids)
            label_ids = self.add_ignored_data(label_ids)

            decoder_attention_mask = (dec_input_ids != self.pad_index)

            
        return {'input_ids': torch.tensor(input_ids, dtype=torch.long),
                'decoder_input_ids': torch.tensor(dec_input_ids, dtype=torch.long),
                'labels': torch.tensor(label_ids, dtype=torch.long),
                'attention_mask': torch.tensor(attention_mask, dtype=torch.long),
                'decoder_attention_mask': torch.tensor(decoder_attention_mask, dtype=torch.long)}

    def __len__(self):
        return self.len