from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
import numpy as np
import pandas as pd
import torch

from transformers import (
    set_seed,
    BartForConditionalGeneration,
    PreTrainedTokenizerFast,
    AutoTokenizer
)

from dataset.QGDataset import QGDataset

MODEL_NAME = "Sehong/kobart-QuestionGeneration"
# MODEL_NAME = "Sehong/t5-large-QuestionGeneration"
TRAIN_DATASET_NAME = "2024-level3-finalproject-nlp-8/squad_kor_v1_train_reformatted"
TEST_DATASET_NAME = "2024-level3-finalproject-nlp-8/squad_kor_v1_test_reformatted"
MODEL_TYPE = "BART"  # ['T5', 'BART']
INPUT_MAX_LEN = 512
BATCH_SIZE = 2
HF_ACCESS_TOKEN = "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"
SEED = 8
OUTPUT_PATH = "../output.csv"

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

    print('bleu1: ', np.mean(bleu1_list))
    print('bleu2: ', np.mean(bleu2_list))
    print('bleu3: ', np.mean(bleu3_list))
    print('bleu4: ', np.mean(bleu4_list))
    print('ROUGE-1: ', np.mean(rouge1_list))
    print('ROUGE-2: ', np.mean(rouge2_list))
    print('ROUGE-L: ', np.mean(rougeL_list))


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
    set_seed(SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # load model
    model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)
    model.to(device)

    # load tokenizer
    tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_NAME)

    # load dataset
    test_dataset = QGDataset(
                        dataset_name=TEST_DATASET_NAME,
                        tokenizer_name=MODEL_NAME,
                        input_max_len = INPUT_MAX_LEN,
                        train=False,
                        model_type=MODEL_TYPE,
                        token=HF_ACCESS_TOKEN
                   )

    # generate question
    generated_questions, labels = inference(model, test_dataset, tokenizer, batch_size=BATCH_SIZE)

    # evaluation model performances
    evaluate(labels, generated_questions)

    # save prediction result
    output = pd.DataFrame({'question': generated_questions, 'label': labels})
    output.to_csv(OUTPUT_PATH, index=False)
    