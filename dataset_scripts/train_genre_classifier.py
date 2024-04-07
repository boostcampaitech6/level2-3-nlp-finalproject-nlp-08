'''
    klue/bert-base를 문학작품과 비문학작품을 구분하는 모델로 파인튜닝해주는 학습 코드입니다.
'''
import torch
from transformers import AutoTokenizer, BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset
import numpy as np
import pandas as pd

# 데이터셋을 불러옴. label 칼럼이 있어야 함.
dataset = load_dataset("2024-level3-finalproject-nlp-8/genre_classifier_train", use_auth_token=True)

# Define BERT model and tokenizer
model_name = "klue/bert-base"
tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Define preprocessing function
def preprocess_function(examples):
    labels = [0 if v=='literature' else 1 for v in examples['label']]
    examples = tokenizer(examples['context'], padding="max_length", truncation=True)
    examples['label'] = np.array(labels)
    return examples

# Preprocess dataset
encoded_dataset = dataset.map(preprocess_function, batched=True)
train_dataset = Dataset.from_pandas(pd.DataFrame(encoded_dataset["train"])[:1800])
dev_dataset = Dataset.from_pandas(pd.DataFrame(encoded_dataset["train"])[1800:])


# Define training arguments
training_args = TrainingArguments(
    output_dir="./ContextClassifierCheckPoint",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=50,
    weight_decay=0.01,
    logging_dir="./logs",
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=dev_dataset
)

# Train the model
trainer.train()

# Evaluate the model
results = trainer.evaluate()
print(results)
