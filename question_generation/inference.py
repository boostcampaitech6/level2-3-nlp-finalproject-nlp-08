import pandas as pd
import torch

from transformers import (
    BartForConditionalGeneration,
    PreTrainedTokenizerFast
)

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, data_path, tokenizer, max_len):
        self.dataset = pd.read_csv(data_path)
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __getitem__(self, idx):
        data = self.dataset.iloc[idx]
        context, answer = data['context'], data['answer']
        raw_input_ids = self.tokenizer.encode(context + '<unused0>' + answer)
        padding = [tokenizer.pad_token_id] * (max_len - len(raw_input_ids))
        input_ids = [tokenizer.bos_token_id] + raw_input_ids + padding + [tokenizer.eos_token_id]

        return torch.tensor([input_ids])
    
    def __len__(self):
        return len(self.dataset)


def inference(model, dataset, tokenizer):
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=False)
    
    model.eval()
    
    questions = []
    for _, data in enumerate(dataloader):
        with torch.no_grad():
            output = model.generate(data)
        question = tokenizer.decode(output.squeeze().tolist(), skip_special_tokenz=True)
        questions.append(question)

    return questions

if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # load model
    model_path = "Sehong/kobart-QuestionGeneration"
    model = BartForConditionalGeneration.from_pretrained(model_path)
    model.to(device)

    # load tokenizer
    tokenizer_name = "Sehong/kobart-QuestionGeneration"
    tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_name)

    # load dataset
    max_len = 512
    data_path = "data.csv"
    dataset = MyDataset(data_path, tokenizer, max_len)

    # generate question
    generated_questions = inference(model, dataset, tokenizer)

    output_path = "./output.csv"
    output = pd.DataFrame({'question': generated_questions})
    output.to_csv(output_path, index=False)
    