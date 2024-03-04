import torch
# import wandb
import pickle as pickle
from transformers import Trainer, TrainingArguments
from utils import set_seed
from data import CustomDataset
from datasets import load_dataset
from transformers import BartForConditionalGeneration, BartTokenizerFast, AutoTokenizer, PreTrainedTokenizerFast
from preprocessing import preprocessing_dataset

def train():
    # seed 고정
    set_seed(42)

    MODEL_NAME = "Sehong/kobart-QuestionGeneration"
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(f'start training {MODEL_NAME} on :',device)
    
    # wandb project name
    # wandb.init(project="final_project") 
    # wandb.run.name = MODEL_NAME
    
    # 데이터셋 불러오기
    dataset = load_dataset("squad_kor_v1")
    temp_train_dataset = preprocessing_dataset(dataset['train'][:10000])
    print('----------Complete train----------')
    temp_valid_dataset = preprocessing_dataset(dataset['validation'][:100])
    print('----------Complete dev----------')
    max_len = 512
    train_dataset = CustomDataset(temp_train_dataset, tokenizer=MODEL_NAME, max_len=max_len)
    valid_dataset = CustomDataset(temp_valid_dataset, tokenizer=MODEL_NAME, max_len=max_len)
    
    # 모델 불러오기   
    model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)
    model.to(device)

    print(model)

    # TrainingArguments setup
    training_args = TrainingArguments(
        output_dir='./models/KoBART',          # output directory
        save_total_limit=1,              # number of total save model.
        save_steps=500,                 # model saving step.
        num_train_epochs=10,              # total number of training epochs
        learning_rate=2e-5,               # learning_rate
        per_device_train_batch_size=5,  # batch size per device during training
        per_device_eval_batch_size=5,   # batch size for evaluation
        warmup_steps=100,                # number of warmup steps for learning rate scheduler
        weight_decay=0.05,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        logging_steps=100,              # log saving step.
        evaluation_strategy='steps', # evaluation strategy to adopt during training
                                    # `no`: No evaluation during training.
                                    # `steps`: Evaluate every `eval_steps`.
                                    # `epoch`: Evaluate every end of epoch.
        eval_steps = 100,            # evaluation step.
    )

    trainer = Trainer(
        model=model,                         # the instantiated 🤗 Transformers model to be trained
        args=training_args,                  # training arguments, defined above
        train_dataset=train_dataset,         # training dataset
        eval_dataset=valid_dataset,             # evaluation dataset
    )

    # train start
    trainer.train()
    model.save_pretrained('./best_model')
    
if __name__ == '__main__':
    train()