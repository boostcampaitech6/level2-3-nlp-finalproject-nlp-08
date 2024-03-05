import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
import numpy as np
import pandas as pd

def eval_scores(reference, candidate):
    rouge = Rouge()
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

test_data_path = ""
output_data_path = ""

test_df = pd.read_csv(test_data_path)
question = list(test_df['question'])

output_df = pd.read_csv(output_data_path)
generated_question = list(output_df['question'])

len_questions = len(question)

bleu1_list = np.zeros(len_questions)
bleu2_list = np.zeros(len_questions)
bleu3_list = np.zeros(len_questions)
bleu4_list = np.zeros(len_questions)
rouge1_list = np.zeros(len_questions)
rouge2_list = np.zeros(len_questions)
rougeL_list = np.zeros(len_questions)


chencherry = SmoothingFunction()

for i in range(len_questions):
    result = eval_scores(question[i], generated_question[i])
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