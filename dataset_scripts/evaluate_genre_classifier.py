'''
    문학작품과 비문학작품을 구분하는 모델을 테스트해보는 코드입니다.
'''
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")
model = AutoModelForSequenceClassification.from_pretrained("2024-level3-finalproject-nlp-8/genre_classifier", num_labels=2)
context = input("지문을 입력하세요: ")
context = tokenizer(context, return_tensors="pt")
model.eval()
with torch.no_grad(): 
    outputs = model(**context)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    if predicted_class == 0:
        print("문학")
    if predicted_class == 1:
        print("비문학")