
import numpy as np
import torch
from datasets import load_dataset

from transformers import AutoTokenizer


import pandas as pd
from tqdm import tqdm

def dict2df(dataset):
    dataset = pd.DataFrame(dataset)
    train_data = pd.DataFrame(columns=['id', 'context', 'question', 'answer', 'answer_start', 'answer_type', 'classtype', 'clue_text', 'clue_start', 'clue_end'])

    for i in tqdm(range(len(dataset))):
        data = dataset.iloc[i]
        id = data['id']
        context = data['context']
        question = data['question']
        answer = data['answers']['text'][0]
        answer_start = data['answers']['answer_start'][0]
        answer_type = None
        classtype = None
        clue_text = None
        clue_start = None
        clue_end = None
        train_data.loc[i] = [id, context, question, answer, answer_start, answer_type, classtype, clue_text, clue_start, clue_end]
    
    return train_data

class QGDataset(torch.utils.data.Dataset):
    def __init__(self, dataset_name, tokenizer_name, input_max_len, train=True, ignore_index=-100):
        
        # temporary dataset loading fuction
        # replace it after building dataset
        if train == True:
            self.dataset = load_dataset(dataset_name)['train'][:10]        
        else:
            self.dataset = load_dataset(dataset_name)['validation'][:10]    

        self.dataset = dict2df(self.dataset)

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
    
    # what is your 정체?
    def add_ignored_data(self, inputs):
        if len(inputs) < self.input_max_len:
            pad = np.array([self.ignore_index] * (self.input_max_len - len(inputs)))
            inputs = np.concatenate([inputs, pad])
        else:
            inputs = inputs[:self.input_max_len]

        return inputs
    
    def __getitem__(self, idx):
        instance = self.dataset.iloc[idx]
        input_ids = self.tokenizer.encode(instance['context'])
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