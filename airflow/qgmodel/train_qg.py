import argparse

import torch
from loguru import logger

from transformers import (
    set_seed, 
    Trainer,
    BartForConditionalGeneration, 
    TrainingArguments,  
    T5ForConditionalGeneration
)

from QGDataset import QGDataset


def train(args):
    set_seed(args.seed)
    
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    logger.info(f"start training {args.model_name} on {device}")

    logger.info(f"load train data : {args.train_dataset_name}")
    logger.info(f"load test data : {args.valid_dataset_name}")
    train_dataset = QGDataset(
                        dataset_name = args.train_dataset_name, 
                        tokenizer_name = args.model_name,
                        input_max_len = args.input_max_len,
                        train=True,
                        model_type=args.model_type, 
                        token = args.hf_access_token,
                    )    
    valid_dataset = QGDataset(
                        dataset_name = args.valid_dataset_name, 
                        tokenizer_name = args.model_name,
                        input_max_len = args.input_max_len,
                        train=False,
                        model_type=args.model_type,
                        token = args.hf_access_token,
                    )
    
    if args.model_type == "BART":
        qg_model = BartForConditionalGeneration.from_pretrained(args.model_name)
    elif args.model_type == "T5":
        qg_model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    

    qg_model.to(device)
    logger.info(f"load question generation model {args.model_name}")
    logger.info(f"model information: {qg_model}")

    # TrainingArguments setup
    training_args = TrainingArguments(
        output_dir=args.output_model_path,   # output directory
        save_total_limit=1,              # number of total save model.
        save_steps=2,                 # model saving step.
        num_train_epochs=4,              # total number of training epochs
        learning_rate=2e-5,               # learning_rate
        per_device_train_batch_size=args.batch_size,  # batch size per device during training
        per_device_eval_batch_size=args.batch_size,   # batch size for evaluation
        warmup_steps=2,                # number of warmup steps for learning rate scheduler
        weight_decay=0.05,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        logging_steps=100,              # log saving step.
    )

    trainer = Trainer(
        model=qg_model,                         # the instantiated 🤗 Transformers model to be trained
        args=training_args,                  # training arguments, defined above
        train_dataset=train_dataset,         # training dataset
        eval_dataset=valid_dataset,             # evaluation dataset
    )

    # train start
    logger.info(f"start training question generation model")
    trainer.train()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', default=8, type=int)
    parser.add_argument('--batch_size', default=2, type=int)
    parser.add_argument('--input_max_len', default=512, type=int)
    parser.add_argument('--hf_access_token', default="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", type=str)
    parser.add_argument('--model_type', default="BART", type=str)  # ['T5', 'BART']
    parser.add_argument('--model_name', default="Sehong/kobart-QuestionGeneration", type=str) # "Sehong/t5-large-QuestionGeneration"
    parser.add_argument('--train_dataset_name', default="2024-level3-finalproject-nlp-8/squad_kor_v1_train_reformatted", type=str)
    parser.add_argument('--valid_dataset_name', default="2024-level3-finalproject-nlp-8/squad_kor_v1_test_reformatted", type=str)
    parser.add_argument('--output_model_path', default="./qgmodel1", type=str) # "Sehong/t5-large-QuestionGeneration"

    args = parser.parse_args()
    
    train(args)