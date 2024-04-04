import argparse

import torch
from loguru import logger

from transformers import (
    set_seed, 
    Trainer,
    BartForConditionalGeneration, 
    TrainingArguments
)

from dataset.QGDataset import QGDataset
from model import QuantizedBART

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
    
    
    qg_model = QuantizedBART.from_pretrained(args.model_name)
    qg_model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
    qg_model.train()
    qg_model = torch.quantization.prepare_qat(qg_model, inplace=True)

    

    qg_model.to(device)
    logger.info(f"load question generation model {args.model_name}")
    logger.info(f"model information: {qg_model}")

    # TrainingArguments setup
    training_args = TrainingArguments(
        output_dir=f'./trained_qg_models/{args.model_name}',   # output directory
        save_total_limit=2,              # number of total save model.
        save_steps=200,                 # model saving step.
        num_train_epochs=1,              # total number of training epochs
        learning_rate=2e-5,               # learning_rate
        per_device_train_batch_size=args.batch_size,  # batch size per device during training
        per_device_eval_batch_size=args.batch_size,   # batch size for evaluation
        warmup_steps=2,                # number of warmup steps for learning rate scheduler
        weight_decay=0.05,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        logging_steps=100,              # log saving step.
        evaluation_strategy='steps', # evaluation strategy to adopt during training
                                    # `no`: No evaluation during training.
                                    # `steps`: Evaluate every `eval_steps`.
                                    # `epoch`: Evaluate every end of epoch.
        eval_steps = 200,            # evaluation step.
        load_best_model_at_end = True
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
    
    # 실제 양자화 모델로 변환
    qg_model.eval()
    qg_model = torch.quantization.convert(qg_model.eval(), inplace=True)
    logger.info(f"finish training question generation model")
    
    # 최종 양자화 모델 저장
    qg_model.save_pretrained(f'./trained_qg_models/{args.model_name}_quantized')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', default=8, type=int)
    parser.add_argument('--batch_size', default=40, type=int)
    parser.add_argument('--input_max_len', default=512, type=int)
    parser.add_argument('--hf_access_token', default="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", type=str)
    parser.add_argument('--model_type', default="BART", type=str)  # ['T5', 'BART']
    parser.add_argument('--model_name', default="Sehong/kobart-QuestionGeneration", type=str) # "Sehong/t5-large-QuestionGeneration"
    parser.add_argument('--train_dataset_name', default="2024-level3-finalproject-nlp-8/squad_kor_v1_train_reformatted", type=str)
    parser.add_argument('--valid_dataset_name', default="2024-level3-finalproject-nlp-8/squad_kor_v1_test_reformatted", type=str)

    args = parser.parse_args()
    
    train(args)