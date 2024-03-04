
import numpy as np
import torch
from datasets import load_dataset

from transformers import AutoTokenizer

class QGDataset(torch.utils.data.Dataset):
    def __init__(self, dataset_name, tokenizer_name, input_max_len, train=True, token=None, ignore_index=-100):
        
        self.dataset = load_dataset(dataset_name, token=token)  
        # temporary setting only 10 sample using!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if train == True:
            self.dataset = self.dataset['train'].to_pandas()[:10] 
        else:
            self.dataset = self.dataset['test'].to_pandas()[:10] 

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        
        self.input_max_len = input_max_len
        self.pad_index = self.tokenizer.pad_token_id
        self.ignore_index = ignore_index
        
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
        input_ids = self.tokenizer.encode(instance['context'] + '<unused0>' + instance['answer'])
        input_ids = self.add_padding_data(input_ids)

        label_ids = self.tokenizer.encode(instance['question'])
        label_ids.append(self.tokenizer.eos_token_id)
        dec_input_ids = [self.tokenizer.eos_token_id]
        dec_input_ids += label_ids[:-1]
        dec_input_ids = self.add_padding_data(dec_input_ids)
        label_ids = self.add_ignored_data(label_ids)

        return {'input_ids': torch.tensor(input_ids, dtype=torch.long),
                'decoder_input_ids': torch.tensor(dec_input_ids, dtype=torch.long),
                'labels': torch.tensor(label_ids, dtype=torch.long)}


    def __len__(self):
        return self.len