import argparse
import json

from loguru import logger
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
import numpy as np
import pandas as pd
import torch

from transformers import (
    set_seed,
    BartForConditionalGeneration,
    T5ForConditionalGeneration,
    PreTrainedTokenizerFast,
    AutoTokenizer
)

from dataset.QGDataset import QGDataset


def eval_scores(reference, candidate):
    rouge = Rouge()
    chencherry = SmoothingFunction()

    rouge_scores = rouge.get_scores(candidate, reference)
    rouge_1 = rouge_scores[0]['rouge-1']['f']  # F1-score
    rouge_2 = rouge_scores[0]['rouge-2']['f']  # F1-score
    rouge_l = rouge_scores[0]['rouge-l']['f']  # F1-score

    reference = [reference.split()]
    candidate = candidate.split()

    bleu1 = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=chencherry.method1)
    bleu2 = sentence_bleu(reference, candidate, weights=(0.5, 0.5, 0, 0), smoothing_function=chencherry.method1)
    bleu3 = sentence_bleu(reference, candidate, weights=(0.33, 0.33, 0.33, 0), smoothing_function=chencherry.method1)
    bleu4 = sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=chencherry.method1)

    result = {
        'bleu1': bleu1,
        'bleu2': bleu2,
        'bleu3': bleu3,
        'bleu4': bleu4,
        'rouge-1': rouge_1,
        'rouge-2': rouge_2,
        'rouge-l': rouge_l
    }
    return result

def evaluate(reference, candidate):

    len_questions = len(candidate)

    bleu1_list = np.zeros(len_questions)
    bleu2_list = np.zeros(len_questions)
    bleu3_list = np.zeros(len_questions)
    bleu4_list = np.zeros(len_questions)
    rouge1_list = np.zeros(len_questions)
    rouge2_list = np.zeros(len_questions)
    rougeL_list = np.zeros(len_questions)


    for i in range(len_questions):
        result = eval_scores(reference[i], candidate[i])
        bleu1_list[i] = result['bleu1']
        bleu2_list[i] = result['bleu2']
        bleu3_list[i] = result['bleu3']
        bleu4_list[i] = result['bleu4']
        rouge1_list[i] = result['rouge-1']
        rouge2_list[i] = result['rouge-2']
        rougeL_list[i] = result['rouge-l']


    logger.info(f'bleu1: {np.mean(bleu1_list)}')
    logger.info(f'bleu2: {np.mean(bleu2_list)}')
    logger.info(f'bleu3: {np.mean(bleu3_list)}')
    logger.info(f'bleu4: {np.mean(bleu4_list)}')
    logger.info(f'ROUGE-1: {np.mean(rouge1_list)}')
    logger.info(f'ROUGE-2: {np.mean(rouge2_list)}')
    logger.info(f'ROUGE-L: {np.mean(rougeL_list)}')

    return result


def inference(model, dataset, tokenizer, batch_size=16):
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)
    
    model.eval()
    
    questions = []
    labels = []
    for _, data in enumerate(dataloader):
        with torch.no_grad():
            for label in data['labels']:
                label = label[label != -100]
                label = tokenizer.decode(label, skip_special_tokens=True)
                labels.append(label)

            output = model.generate(input_ids=data['input_ids'])
            for out in output:
                question = tokenizer.decode(out, skip_special_tokens=True)
                questions.append(question)

    return questions, labels
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', default=8, type=int)
    parser.add_argument('--batch_size', default=2, type=int)
    parser.add_argument('--input_max_len', default=512, type=int)
    parser.add_argument('--output_path', default="../artifacts/output.csv", type=str)
    parser.add_argument('--output_metric_path', default="../artifacts/metric_result.json", type=str)
    parser.add_argument('--hf_access_token', default="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", type=str)
    parser.add_argument('--model_type', default="BART", type=str)  # ['T5', 'BART']
    parser.add_argument('--model_name', default="Sehong/kobart-QuestionGeneration", type=str) # "Sehong/t5-large-QuestionGeneration"
    parser.add_argument('--test_dataset_name', default="2024-level3-finalproject-nlp-8/squad_kor_v1_test_reformatted", type=str)

    args = parser.parse_args()

    set_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # load model
    logger.info(f'load {args.model_name} for evaluation')
    if args.model_type == "BART":
        model = BartForConditionalGeneration.from_pretrained(args.model_name)
    elif args.model_type == "T5":
        qg_model = T5ForConditionalGeneration.from_pretrained(args.model_name)
    model.to(device)

    # load tokenizer
    logger.info(f'load {args.model_name} tokenizer for evaluation')
    tokenizer = PreTrainedTokenizerFast.from_pretrained(args.model_name)

    # load dataset
    logger.info(f'load dataset {args.test_dataset_name} for hugging face')
    test_dataset = QGDataset(
                        dataset_name=args.test_dataset_name,
                        tokenizer_name=args.model_name,
                        input_max_len = args.input_max_len,
                        train=False,
                        model_type=args.model_type,
                        token=args.hf_access_token
                   )

    # generate question
    logger.info(f'generate question sentences')
    generated_questions, labels = inference(model, test_dataset, tokenizer, batch_size=args.batch_size)

    # evaluation model performances
    logger.info(f'evaluate scores on generated questions')
    metric_result = evaluate(labels, generated_questions)

    with open(args.output_metric_path, "w") as outfile: 
        json.dump(metric_result, outfile)

    # save prediction result
    logger.info(f'save prediction csv file {args.output_path}')
    output = pd.DataFrame({'question': generated_questions, 'label': labels})
    output.to_csv(args.output_path, index=False)
    