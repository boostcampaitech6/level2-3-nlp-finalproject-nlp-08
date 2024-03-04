import torch
from torch.utils.data import DataLoader
from loguru import logger

from transformers import set_seed, BartForConditionalGeneration, TrainingArguments, Trainer

from dataset.QGDataset import QGDataset

MODEL_NAME = "Sehong/kobart-QuestionGeneration"
TRAIN_DATASET_NAME = "squad_kor_v1"
VALID_DATASET_NAME = "squad_kor_v1"
INPUT_MAX_LEN = 512
BATCH_SIZE = 2

def train():
    set_seed(8)
    
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    logger.info(f"start training {MODEL_NAME} on {device}")
    

    logger.info(f"load train data : {TRAIN_DATASET_NAME}")
    logger.info(f"load test data : {VALID_DATASET_NAME}")
    train_dataset = QGDataset(
                        dataset_name = TRAIN_DATASET_NAME, 
                        tokenizer_name = MODEL_NAME,
                        input_max_len = INPUT_MAX_LEN,
                        train=True, 
                    )    
    valid_dataset = QGDataset(
                        dataset_name = VALID_DATASET_NAME, 
                        tokenizer_name = MODEL_NAME,
                        input_max_len = INPUT_MAX_LEN,
                        train=False
                    )

    logger.info(f"load train dataloader")
    logger.info(f"load test dataloader")
    train_dataloader = DataLoader(train_dataset, BATCH_SIZE)
    valid_dataloader = DataLoader(valid_dataset, BATCH_SIZE)
    
    
    qg_model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)
    qg_model.to(device)
    logger.info(f"load question generation model {MODEL_NAME}")
    logger.info(f"model information: {qg_model}")

    # TrainingArguments setup
    training_args = TrainingArguments(
        output_dir=f'./trained_qg_models/{MODEL_NAME}',   # output directory
        save_total_limit=2,              # number of total save model.
        save_steps=2,                 # model saving step.
        num_train_epochs=10,              # total number of training epochs
        learning_rate=2e-5,               # learning_rate
        per_device_train_batch_size=BATCH_SIZE,  # batch size per device during training
        per_device_eval_batch_size=BATCH_SIZE,   # batch size for evaluation
        warmup_steps=2,                # number of warmup steps for learning rate scheduler
        weight_decay=0.05,               # strength of weight decay
        logging_dir='./logs',            # directory for storing logs
        logging_steps=100,              # log saving step.
        evaluation_strategy='steps', # evaluation strategy to adopt during training
                                    # `no`: No evaluation during training.
                                    # `steps`: Evaluate every `eval_steps`.
                                    # `epoch`: Evaluate every end of epoch.
        eval_steps = 2,            # evaluation step.
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
    
if __name__ == '__main__':
    train()