
import numpy as np
import torch
from datasets import load_dataset

from transformers import AutoTokenizer

class QGDataset(torch.utils.data.Dataset):
    def __init__(self, dataset_name, tokenizer_name, input_max_len, model_type, train=True, token=None, ignore_index=-100):
        
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
        if self.model_type == 'pipe-line':
            input_text = instance['context'] + '<unused0>' + instance['answer']
            label_text = instance['question']
        
            input_ids = self.tokenizer.encode(input_text)
            input_ids = self.add_padding_data(input_ids)

            label_ids = self.tokenizer.encode(label_text)
            label_ids.append(self.tokenizer.eos_token_id)
            dec_input_ids = [self.tokenizer.eos_token_id]
            dec_input_ids += label_ids[:-1]
            dec_input_ids = self.add_padding_data(dec_input_ids)
            label_ids = self.add_ignored_data(label_ids)

            return {'input_ids': torch.tensor(input_ids, dtype=torch.long),
                    'decoder_input_ids': torch.tensor(dec_input_ids, dtype=torch.long),
                    'labels': torch.tensor(label_ids, dtype=torch.long)}

        elif self.model_type == 'e2e':
            instance = self.docs.iloc[idx]
            content = instance['content']
            question = instance['question'].strip()

            sep_index = content.find('[SEP]')

            answer = content[sep_index + 6::].strip()
            content = content[:sep_index].strip()

            prefix_content_token_id = self.tokenizer.encode('content:', add_special_tokens=False)
            prefix_answer_token_id = self.tokenizer.encode('answer:', add_special_tokens=False)
            prefix_question_token_id = self.tokenizer.encode('question:', add_special_tokens=False)

            input_ids = prefix_answer_token_id
            input_ids += self.tokenizer.encode(answer, add_special_tokens=False)
            input_ids += prefix_content_token_id
            input_ids += self.tokenizer.encode(content, add_special_tokens=False)
            input_ids = self.add_padding_data(input_ids)

            label_ids = prefix_question_token_id
            label_ids += self.tokenizer.encode(question, add_special_tokens=False)
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